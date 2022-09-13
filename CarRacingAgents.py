import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
import cv2

# CNN + Sensors Agent
class CarRacingAgent:
    def __init__(
        self,
        action_space = [0, 1, 2, 3, 4],
        frame_stack_num = 3,
        memory_size = 5000,
        gamma = 0.95, # discount rate
        epsilon = 1.0, # exploration rate
        epsilon_min = 0.1,
        epsilon_decay = 0.9999,
        learning_rate = 0.001,
        name = 'agent_03'
    ):
        self.action_space = action_space
        self.frame_stack_num = frame_stack_num
        self.memory = deque(maxlen=memory_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()
        self.name = name
        
        # Plots
        self.results = []
        self.epsilons = []
        self.episode_durations = []

    def process_state_image(self, state, env):
        state_image = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
        state_image = state_image.astype(float)
        state_image /= 255.0

        ## Sensors
        car_front = [65, 48]
        
        # Speed
        speed = np.sqrt(np.square(env.car.hull.linearVelocity[0]) + np.square(env.car.hull.linearVelocity[1]))

        # Front Sensor
        front_sensor = car_front[0]
        for i in range(car_front[0]):
            pixel = state[car_front[0]-i, car_front[1], :]

            if pixel[1]>pixel[0]*1.3 and pixel[1]>pixel[2]*1.3:
                front_sensor = i
                break

        # Front left sensor
        left_sensor = car_front[0]
        for i in range(car_front[0]):
            pixel = state[car_front[0]-i, car_front[1]-i//4, :]
            if pixel[1]>pixel[0]*1.3 and pixel[1]>pixel[2]*1.3:
                left_sensor = i
                break
            
        # Full left sensor
        full_left_sensor = car_front[1]
        for i in range(car_front[1]):
            pixel = state[car_front[0], car_front[1]-i, :]
            if pixel[1]>pixel[0]*1.3 and pixel[1]>pixel[2]*1.3:
                full_left_sensor =  i
                break

        # Front Right Sensor
        right_sensor = car_front[0]
        for i in range(car_front[0]):
            pixel = state[car_front[0]-i, car_front[1]+i//4, :]
            if pixel[1]>pixel[0]*1.3 and pixel[1]>pixel[2]*1.3:
                right_sensor = i
                break
        
        # Full right sensor
        full_right_sensor = 96-car_front[1]
        for i in range(96-car_front[1]):
            pixel = state[car_front[0], car_front[1]+i, :]
            if pixel[1]>pixel[0]*1.3 and pixel[1]>pixel[2]*1.3:
                full_right_sensor = i
                break

        state_sensors = [round(speed, 2), front_sensor, left_sensor, full_left_sensor, right_sensor, full_right_sensor]

        return [state_image, state_sensors]

    def generate_state_frame_stack_from_queue(self, deque):
        state_image = []
        state_sensors = []
        for a in deque:
            state_image.append(a[0])
            state_sensors.append(a[1])

        frame_stack_image = np.array(state_image)
        frame_stack_sensor = np.array(state_sensors)

        # Move stack dimension to the channel dimension (stack, x, y) -> (x, y, stack)
        return [np.transpose(frame_stack_image, (1, 2, 0)), np.transpose(frame_stack_sensor, (1, 0))]
        

    def build_model(self):
        # Neural Network for Deep-Q learning Model
        
        input_images = tf.keras.layers.Input(((96, 96, self.frame_stack_num)))
        input_sensors = tf.keras.layers.Input(((6, self.frame_stack_num)))
        
        x = Conv2D(filters=6, kernel_size=(7, 7), strides=3, activation='relu', input_shape=(96, 96, self.frame_stack_num))(input_images)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Conv2D(filters=12, kernel_size=(4, 4), activation='relu')(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Flatten()(x)
        output1 = Dense(216, activation='relu')(x)

        # Add sensors
        concatted = tf.keras.layers.Concatenate()([output1, input_sensors[:,:,-1]]) # Use only lastest sensors
        
        x = Dense(32, activation='relu')(concatted)
        outputs = Dense(len(self.action_space), activation=None)(x)

        model = tf.keras.Model([input_images, input_sensors], outputs)
        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=self.learning_rate, epsilon=1e-7))

        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, self.action_space.index(action), reward, next_state, done))

    def act(self, state):
        if np.random.rand() > self.epsilon:
            act_values = self.model.predict([np.expand_dims(state[0], axis=0), np.expand_dims(state[1], axis=0)], verbose=0)
            action_index = np.argmax(act_values[0])
        else:
            action_index = random.randrange(len(self.action_space))
        return self.action_space[action_index]

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        state_pairs = list(zip(*minibatch))[0]
        state_images = np.stack(list(zip(*state_pairs))[0], axis=0)
        state_sensors = np.stack(list(zip(*state_pairs))[1], axis=0)
        states = [state_images, state_sensors]

        action_indexes = list(zip(*minibatch))[1]
        rewards = list(zip(*minibatch))[2]

        next_state_pairs = list(zip(*minibatch))[3]
        next_state_images = np.stack(list(zip(*next_state_pairs))[0], axis=0)
        next_state_sensors = np.stack(list(zip(*next_state_pairs))[1], axis=0)
        next_states = [next_state_images, next_state_sensors]

        dones = list(zip(*minibatch))[4]

        target = self.model.predict(states, verbose=0)
        t = self.model.predict(next_states, verbose=0)

        for idx, (_, _, _, _, _) in enumerate(minibatch):
            if dones[idx]:
                target[idx][action_indexes[idx]] = rewards[idx]
            else:
                target[idx][action_indexes[idx]] = rewards[idx] + self.gamma*np.amax(t[idx])

        self.model.fit(states, target, epochs=1, verbose=0)
  
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)
        self.update_target_model()

    def save(self, name):
        self.target_model.save_weights(name)
