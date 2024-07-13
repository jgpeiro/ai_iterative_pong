# Pong Game Software Design Document

![Alt text](png/gameplay.png?raw=true "Title")

https://www.youtube.com/watch?v=Jzg7LhgocyI

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Class Descriptions](#class-descriptions)
4. [Game States](#game-states)
5. [User Interface](#user-interface)
6. [Audio System](#audio-system)
7. [Power-Up System](#power-up-system)
8. [Particle System](#particle-system)
9. [AI Component](#ai-component)
10. [Hardware Integration](#hardware-integration)
11. [Performance Considerations](#performance-considerations)
12. [Future Enhancements](#future-enhancements)

## 1. Introduction

This document describes the software design for a modern interpretation of the classic Pong game, implemented in MicroPython for a custom hardware platform. The game features a single-player mode against an AI opponent, power-ups, particle effects, and an audio system, providing an engaging and dynamic gaming experience.

## 2. System Architecture

The Pong game system is composed of several interconnected components, each responsible for specific aspects of the game's functionality. Below is a high-level overview of the system architecture:

![Alt text](png/system_architecture.png?raw=true "Title")

The main game loop orchestrates the overall flow of the game, managing state transitions and coordinating updates to all game components. It interfaces with hardware inputs to gather user actions and sends rendering commands to the display output.

## 3. Class Descriptions

### 3.1 Pong

The `Pong` class serves as the central controller for the game, managing game states, score tracking, and coordinating updates to all game objects.

![Alt text](png/class_pong.png?raw=true "Title")

### 3.2 Paddle

The `Paddle` class represents a player's paddle, handling movement, power-up effects, and rendering.

![Alt text](png/class_paddle.png?raw=true "Title")

### 3.3 Ball

The `Ball` class manages the ball's position, velocity, and interactions with paddles and walls.

![Alt text](png/class_ball.png?raw=true "Title")

### 3.4 PowerUp

The `PowerUp` class represents power-up items that appear during gameplay, providing various effects when collected.

![Alt text](png/class_power_up.png?raw=true "Title")

### 3.5 ParticleSystem

The `ParticleSystem` class manages visual effects, creating and updating particles for various game events.

![Alt text](png/class_particle_system.png?raw=true "Title")

### 3.6 AudioEngine

The `AudioEngine` class manages sound generation and playback for various game events.

![Alt text](png/class_audio_engine.png?raw=true "Title")

## 4. Game States

The game transitions between different states, each with its own update and draw logic:

![Alt text](png/game_states.png?raw=true "Title")

1. **Welcome**: Displays game instructions and waits for user input to start the game.
2. **Playing**: The main gameplay state where the game logic is updated and rendered.
3. **Paused**: Halts gameplay and displays a pause menu with options to resume or return to the welcome screen.
4. **Goal**: Triggered when a goal is scored, displaying an animation before resuming play.

## 5. User Interface

The user interface is primarily handled by the `draw` methods of various classes, rendering game elements on the LCD screen. Key UI components include:

1. Paddles and balls
2. Score displays (using seven-segment display simulation)
3. Power-up indicators
4. Particle effects
5. Debug information (when enabled)
6. Welcome screen with scrolling instructions
7. Pause menu
8. Goal animation

## 6. Audio System

The audio system uses PWM (Pulse Width Modulation) to generate sound effects for various game events. It supports multiple sound generators, allowing for concurrent audio playback.

![Alt text](png/audio_system.png?raw=true "Title")

Each sound generator uses an ADSR (Attack, Decay, Sustain, Release) envelope for shaping the sound, providing more dynamic and interesting audio feedback.

## 7. Power-Up System

The power-up system adds variety and strategic depth to the gameplay. Power-ups appear randomly on the screen and can be collected by paddles. Types of power-ups include:

1. Grow: Increases paddle size
2. Shrink: Decreases paddle size
3. Magnet: Attracts or repels the ball
4. Control: Allows the paddle to temporarily "catch" the ball
5. Speed: Increases ball speed
6. Multiball: Adds an additional ball to the game

Power-ups are managed by the `Pong` class, which handles their creation, movement, collision detection, and application of effects.

## 8. Particle System

The particle system enhances visual feedback by creating small, animated particles for various game events:

1. Paddle hits
2. Wall bounces
3. Power-up collections
4. Goal celebrations

Particles are managed by the `ParticleSystem` class, which handles their creation, updating, and rendering.

## 9. AI Component

The AI opponent is implemented within the `Pong` class's `update_ai` method. It uses a simple tracking algorithm to move the AI-controlled paddle towards the ball's position. The AI difficulty can be adjusted, affecting the speed and responsiveness of the AI paddle.

![Alt text](png/ai_component.png?raw=true "Title")

## 10. Hardware Integration

The game interfaces with hardware components for input and output:

![Alt text](png/hardware_integration.png?raw=true "Title")

Input is polled in the main game loop and passed to the `Pong` class's `update` method. The LCD display is updated at the end of each game loop iteration.

## 11. Performance Considerations

To maintain smooth gameplay on the limited hardware:

1. The game uses a frame rate of approximately 100 FPS (10ms sleep between frames).
2. Particle effects are limited to a maximum number of particles.
3. The audio system removes inactive sound generators to conserve resources.
4. Debug information can be toggled on/off to reduce rendering overhead when not needed.

## 12. Future Enhancements

Potential areas for future improvement include:

1. Networked multiplayer support
2. Additional power-up types and effects
3. Multiple AI difficulty levels with more sophisticated behaviors
4. High score tracking and persistent storage
5. Customizable paddle and ball appearances
6. Background music with volume control
7. Menu system for game options and customization

This modular design allows for easy expansion and modification of game features, providing a solid foundation for future development.





# Pong Game Execution Behavior

This document provides a detailed explanation of the execution behavior of the Pong game, from the initial `asyncio.run(main())` call through the goal animation sequence. We'll examine the relationships between all elements, events, and data flow using a top-down approach with diagrams and flowcharts at different levels of abstraction.

## Table of Contents
1. [Top-Level Execution Flow](#top-level-execution-flow)
2. [Detailed Main Loop Execution](#detailed-main-loop-execution)
3. [State Transitions](#state-transitions)
4. [Data Flow Between Classes](#data-flow-between-classes)
5. [Detailed Goal Animation Sequence](#detailed-goal-animation-sequence)
6. [Summary](#summary)

## Top-Level Execution Flow

The game's execution begins with the `asyncio.run(main())` call, which initializes the LCD display and creates a Pong game instance. It then enters the main game loop, which continues until the game is no longer running. In each iteration of this loop, the game checks its current state (Welcome, Playing, Paused, or Goal) and updates accordingly. After updating, it draws the current state and displays it on the LCD. This process repeats, with the game constantly checking if it should continue running or end.

The highest level of abstraction shows the overall flow of the game:

![Alt text](png/top_level_execution_flow.png?raw=true "Title")

This flowchart illustrates the main execution flow of the game:
1. The game starts with the `asyncio.run(main())` call.
2. It initializes the LCD and creates a Pong game instance.
3. The main game loop begins, which continues until the game is no longer running.
4. In each iteration, it checks the current game state and updates accordingly.
5. After updating, it draws the current state and displays it on the LCD.

## Detailed Main Loop Execution

Each iteration of the main game loop follows a specific sequence of operations. It starts by polling hardware inputs to determine user actions. Based on the current state and input, it updates game elements accordingly. For the Welcome state, it updates the welcome screen. In the Playing state, it updates game elements such as paddles, balls, and power-ups. The Paused state updates the pause menu, while the Goal state updates the goal animation. After updating, it draws the current state, then updates the particle system for visual effects. The game calculates the current frame rate (FPS) and updates the audio engine for sound effects. Finally, it refreshes the LCD display and sleeps for 10ms before starting the next iteration. This process continues until the game is no longer running.

A more detailed look at what happens in each iteration of the main game loop:

![Alt text](png/detailed_main_loop_execution.png?raw=true "Title")

This flowchart provides more detail on each loop iteration:
1. The loop starts by polling hardware inputs to determine user actions.
2. Based on the current state and input, it updates game elements accordingly.
3. After updating, it draws the current state, updates the particle system and audio engine.
4. Finally, it refreshes the LCD display and sleeps for 10ms before the next iteration.

## State Transitions

The game transitions between different states based on events and user inputs. It starts in the Welcome state and moves to the Playing state when any button is pressed. From the Playing state, it can transition to the Paused state if the center joystick is pressed, or to the Goal state if a ball reaches the edge of the screen. In the Paused state, pressing the A button returns to Playing, while pressing B returns to the Welcome screen. The Goal state automatically returns to Playing once the animation is complete. The game can end from the Playing state under certain conditions.

The game transitions between different states based on events and user inputs:

![Alt text](png/game_state_transitions.png?raw=true "Title")

This state diagram shows how the game moves between different states:
- It starts in the Welcome state and moves to Playing when any button is pressed.
- From Playing, it can transition to Paused or Goal states.
- The Goal state automatically returns to Playing once the animation is complete.
- The game can end from the Playing state.

## Data Flow Between Classes

The `Pong` class acts as the central controller in the game, interacting with all other classes. It manages instances of Paddle, Ball, PowerUp, ParticleSystem, AudioEngine, and SevenSegmentDisplay classes. Paddles interact with balls for collision detection and with power-ups for special effects. Both ball-paddle collisions and power-up collections can trigger particle effects (managed by ParticleSystem) and sound effects (managed by AudioEngine). The Pong class also handles the score display using SevenSegmentDisplay instances. It receives input from hardware (like joystick and buttons) and sends output to the LCD display. This centralized structure allows the Pong class to coordinate all aspects of the game, from physics simulations to visual and audio output.

The following diagram illustrates how data flows between the main classes in the game:

![Alt text](png/data_flow_between_classes.png?raw=true "Title")

Key points about data flow:
- The `Pong` class acts as the central controller, interacting with all other classes.
- Paddles interact with balls and power-ups, triggering particle effects and audio cues.
- The `Pong` class manages the score display and interacts with hardware input and LCD output.

## Detailed Goal Animation Sequence

When a goal is scored, a specific sequence of events occurs. First, the Pong class detects the goal and removes the scoring ball. It then changes the game state to "goal" and triggers the creation of celebration particles through the ParticleSystem. The AudioEngine is instructed to play a goal sound. For each frame of the animation, the Pong class updates the animation state, including the particles. It then draws the "GOAL!" text with rainbow colors, an expanding circle animation, any remaining game objects (like paddles, other balls, and power-ups), and the particles. This is all sent to the LCD display for rendering. This animation sequence repeats for a set number of frames. After the animation completes, the Pong class resets the ball position and changes the game state back to "playing", resuming normal gameplay.

When a goal is scored, the following sequence of events occurs:

![Alt text](png/goal_animation_sequence.png?raw=true "Title")

This sequence diagram shows the detailed steps during a goal animation:
1. The `Pong` class detects a goal and removes the scoring ball.
2. It changes the game state to "goal" and triggers particle and sound effects.
3. For each frame of the animation, it updates and draws various visual elements.
4. After the animation, it resets the ball position and returns to the "playing" state.

## Summary

The execution behavior of the Pong game is a complex interplay of various components, all orchestrated by the central Pong class. Starting from the asyncio.run(main()) call, the game initializes and enters a main loop that continually updates and renders the game state. It smoothly transitions between different states (Welcome, Playing, Paused, and Goal) based on game events and user inputs. The game manages multiple elements including paddles, balls, power-ups, particles, and audio, coordinating their interactions in real-time. Special sequences, like the goal animation, temporarily take over the game flow to provide engaging feedback to the player. Throughout all of this, the Pong class acts as the central hub, managing state transitions, coordinating all game elements, and ensuring smooth gameplay. This structure allows for a dynamic and responsive game experience, balancing complex interactions with performance considerations on the limited hardware.

The execution behavior of the Pong game can be summarized as follows:

1. The game starts with `asyncio.run(main())`, initializing the LCD and Pong game.
2. The main game loop continuously polls for input and updates the game state.
3. Different update and draw routines are called depending on the current state (welcome, playing, paused, or goal).
4. The game manages various elements like paddles, balls, power-ups, particles, and audio, coordinating their interactions.
5. When a goal is scored, the game enters a special goal animation state, creating visual and audio effects before resuming play.
6. Throughout the game, the `Pong` class acts as the central controller, managing state transitions and coordinating all game elements.

This multi-level view provides a comprehensive understanding of how all elements interact, from the highest-level flow down to specific sequences like the goal animation. The relationships between classes are primarily managed through the `Pong` class, which acts as a central hub for game logic and state management.





# Pong Game Engine Analysis

This document provides a comprehensive analysis of the Pong game engine, focusing on its asyncio-based structure, capabilities, PWM handling, memory management, and real-time performance.

## Table of Contents
1. [Asyncio-based Game Loop](#asyncio-based-game-loop)
2. [PWM Handling for Audio](#pwm-handling-for-audio)
3. [Memory Management](#memory-management)
4. [Real-time Performance](#real-time-performance)
5. [Capabilities and Extensibility](#capabilities-and-extensibility)
6. [Limitations and Potential Improvements](#limitations-and-potential-improvements)

## Asyncio-based Game Loop

The game engine utilizes Python's asyncio library to create an asynchronous game loop. This approach allows for efficient handling of multiple tasks without blocking the main execution thread.


![Alt text](png/asyncio_based_game_loop.png?raw=true "Title")


The main game loop is implemented as an asynchronous function:

```python
async def main():
    lcd = st7789_fb.LCD()
    pong = Pong()
    lcd.show()
    
    while pong.is_running():
        # Handle input, update game state, draw, etc.
        await pong.update(event)
        pong.draw(lcd)
        lcd.show()
        
        await asyncio.sleep_ms(10)
```

Key aspects of the asyncio-based game loop:

1. **Non-blocking execution**: The `await` keyword is used for potentially blocking operations, allowing other tasks to run in the meantime.
2. **Consistent frame rate**: The `asyncio.sleep_ms(10)` call ensures a consistent frame rate of approximately 100 FPS.
3. **Event-driven updates**: The game state is updated based on events, which are determined by polling hardware inputs.
4. **Asynchronous audio updates**: The audio engine is updated asynchronously, preventing audio processing from blocking the main game loop.

## PWM Handling for Audio

The game engine uses Pulse Width Modulation (PWM) for audio generation. This is handled through the `AudioEngine` and various `SoundGenerator` classes.

![Alt text](png/pwm_handling_for_audio.png?raw=true "Title")


Key aspects of PWM handling:

1. **Multiple sound generators**: The `AudioEngine` can manage multiple `SoundGenerator` instances, allowing for concurrent sounds.
2. **ADSR envelope**: Each `SoundGenerator` uses an Attack-Decay-Sustain-Release (ADSR) envelope for shaping the sound.
3. **Frequency and volume control**: The PWM frequency and duty cycle are adjusted to control the pitch and volume of the generated sound.
4. **Asynchronous updates**: The `update` method of `AudioEngine` is called asynchronously in the main game loop, preventing audio processing from blocking other game operations.

Example of PWM initialization and usage:

```python
class SoundGenerator:
    def __init__(self, pin_number):
        self.pwm = machine.PWM(machine.Pin(pin_number))
        self.pwm.freq(440)  # Default frequency
        self.pwm.duty_u16(0)  # Start silent

    async def update(self, dt):
        level = self._calculate_envelope_level()
        duty = int(level * self.volume * 655.35)  # Scale to 16-bit duty cycle
        self.pwm.duty_u16(duty)
```

## Memory Management

The game engine needs to be efficient with memory usage due to the limited resources of the hardware platform. Here are key aspects of memory management in the engine:

1. **Object reuse**: Instead of creating new objects frequently, the engine reuses existing objects when possible. For example, the `Ball` and `Paddle` objects are created once and updated, rather than recreated each frame.

2. **Particle system limits**: The `ParticleSystem` has a maximum number of particles, replacing old particles when the limit is reached:

```python
class ParticleSystem:
    def __init__(self, max_particles=100):
        self.particles = []
        self.max_particles = max_particles

    def add_particle(self, x, y, vx, vy, color, lifetime):
        if len(self.particles) < self.max_particles:
            self.particles.append(Particle(x, y, vx, vy, color, lifetime))
        else:
            # Replace the oldest particle
            self.particles.pop(0)
            self.particles.append(Particle(x, y, vx, vy, color, lifetime))
```

3. **Garbage collection**: The engine periodically calls `gc.collect()` to manage memory:

```python
import gc

# In the main game loop
gc.collect()
```

4. **Efficient data structures**: The engine uses simple data structures like lists and dictionaries, avoiding complex objects that might consume more memory.

## Real-time Performance

The game engine is designed to maintain real-time performance on limited hardware. Key strategies include:

1. **Fixed time step**: The main loop uses a fixed time step of 10ms, ensuring consistent updates:

```python
await asyncio.sleep_ms(10)
```

2. **Asynchronous operations**: Using asyncio allows for non-blocking operations, improving responsiveness.

3. **Efficient rendering**: The engine uses a framebuffer for rendering, updating the entire screen at once rather than pixel-by-pixel.

4. **Performance monitoring**: The engine includes an FPS counter and memory usage display for debugging:

```python
self.frame_count += 1
if self.frame_count == 30:
    current_time = time.ticks_ms()
    self.fps = 30000 / (current_time - self.last_time)
    self.last_time = current_time
    self.frame_count = 0
```

5. **Optimized collision detection**: The engine uses simple rectangle-based collision detection for efficiency.

## Capabilities and Extensibility

The game engine demonstrates several capabilities that make it extensible:

1. **State management**: The engine can handle multiple game states (Welcome, Playing, Paused, Goal) seamlessly.

2. **Power-up system**: The engine includes a flexible power-up system that can be easily extended with new types of power-ups.

3. **Particle system**: The particle system adds visual flair and can be used for various effects.

4. **Audio engine**: The audio system supports multiple concurrent sounds with ADSR envelopes.

5. **AI opponent**: The engine includes a simple AI opponent that could be extended for more complex behavior.

## Limitations and Potential Improvements

While the game engine is well-designed for its purpose, there are some limitations and areas for potential improvement:

1. **Single-threaded**: Despite using asyncio, the engine is still essentially single-threaded. True multi-threading could potentially improve performance on multi-core systems.

2. **Fixed time step**: While the fixed time step ensures consistency, it may not adapt well to varying system loads. A variable time step with interpolation could provide smoother performance across different devices.

3. **Limited audio capabilities**: The PWM-based audio is quite basic. A more advanced audio system could provide better sound quality.

4. **2D-only**: The engine is designed for 2D games only. Extending to 3D would require significant changes.

5. **Limited physics**: The physics simulations are very basic. A more robust physics engine could enable more complex gameplay.

In conclusion, the Pong game engine demonstrates effective use of asyncio for game development on limited hardware. Its design allows for responsive gameplay while managing audio, particle effects, and game state. While there are areas for potential improvement, the engine provides a solid foundation for creating simple 2D games with real-time interactions.











# Attack-Decay-Sustain-Release (ADSR) Envelope and PWM Implementation

## Table of Contents
1. [ADSR Envelope Overview](#adsr-envelope-overview)
2. [ADSR Implementation in the Pong Game Engine](#adsr-implementation-in-the-pong-game-engine)
3. [PWM Signal Properties and ADSR](#pwm-signal-properties-and-adsr)
4. [Mathematical Representation](#mathematical-representation)
5. [Performance Considerations](#performance-considerations)

## ADSR Envelope Overview

The Attack-Decay-Sustain-Release (ADSR) envelope is a common technique used in sound synthesis to shape the amplitude of a sound over time. It consists of four phases:

1. **Attack**: The initial rise from zero to peak amplitude
2. **Decay**: The subsequent drop to the sustain level
3. **Sustain**: The constant amplitude held while a note is played
4. **Release**: The final drop from the sustain level back to zero

Here's a visual representation of an ADSR envelope:

```
Amplitude
    ^
    |    /\
    |   /  \
    |  /    \___________
    | /                 \
    |/                   \
    +-----------------------> Time
      A    D    S         R
```

## ADSR Implementation in the Pong Game Engine

In the Pong game engine, the ADSR envelope is implemented in the `SoundGenerator` class. Here's the relevant code:

```python
class SoundGenerator:
    def __init__(self, pin_number):
        self.pwm = machine.PWM(machine.Pin(pin_number))
        self.pwm.freq(440)  # Default frequency
        self.pwm.duty_u16(0)  # Start silent
        
        self.volume = 50
        self.attack = 0.01
        self.decay = 0.1
        self.sustain = 0.7
        self.release = 0.3
        
        self.current_time = 0
        self.is_note_on = False
        self.envelope_stage = 'off'

    async def update(self, dt):
        level = self._calculate_envelope_level()
        duty = int(level * self.volume * 655.35)  # Scale to 16-bit duty cycle
        self.pwm.duty_u16(duty)
        
        self.current_time += dt

    def _calculate_envelope_level(self):
        if self.envelope_stage == 'attack':
            level = min(1, self.current_time / self.attack)
            if level >= 1:
                self.envelope_stage = 'decay'
        elif self.envelope_stage == 'decay':
            level = max(self.sustain, 1 - (1 - self.sustain) * (self.current_time - self.attack) / self.decay)
            if level <= self.sustain:
                self.envelope_stage = 'sustain'
        elif self.envelope_stage == 'sustain':
            level = self.sustain
        elif self.envelope_stage == 'release':
            level = max(0, self.sustain * (1 - (self.current_time / self.release)))
            if level <= 0:
                self.envelope_stage = 'off'
        else:
            level = 0
        return level
```

The ADSR envelope is implemented by calculating the appropriate amplitude level based on the current time and the envelope stage. The `_calculate_envelope_level()` method determines the current amplitude level, which is then used to set the PWM duty cycle.

## PWM Signal Properties and ADSR

Pulse Width Modulation (PWM) is used to generate audio signals in this implementation. PWM works by rapidly switching a digital signal between on and off states. The ratio of the "on" time to the total cycle time (on + off) is called the duty cycle.

In audio applications, PWM takes advantage of two key properties:

1. **Averaging effect**: When a PWM signal is passed through a low-pass filter (which could be as simple as a speaker's natural frequency response), it produces an analog-like output that's proportional to the duty cycle.

2. **Frequency control**: The frequency of the PWM signal determines the pitch of the sound.

The ADSR envelope modulates the duty cycle of the PWM signal over time, which in turn modulates the amplitude of the resulting sound. The relationship between duty cycle and perceived volume is approximately linear, which simplifies the implementation.

## Mathematical Representation

Let's define the ADSR envelope mathematically:

1. **Attack**: For $0 \leq t < A$
   $$ f(t) = \frac{t}{A} $$

2. **Decay**: For $A \leq t < A + D$
   $$ f(t) = 1 - (1 - S) \cdot \frac{t - A}{D} $$

3. **Sustain**: For $A + D \leq t < A + D + S$
   $$ f(t) = S $$

4. **Release**: For $A + D + S \leq t < A + D + S + R$
   $$ f(t) = S \cdot (1 - \frac{t - (A + D + S)}{R}) $$

Where:
- $t$ is the current time
- $A, D, S, R$ are the Attack, Decay, Sustain, and Release parameters respectively

The PWM duty cycle is then calculated as:

$$ duty = f(t) \cdot volume \cdot 655.35 $$

The factor 655.35 comes from scaling the 0-100 volume range to the 0-65535 range used by the 16-bit PWM.

## Performance Considerations

The ADSR implementation in this game engine is designed to be computationally efficient:

1. **Linear interpolation**: The envelope uses simple linear interpolation, which is fast to compute.

2. **Minimal branching**: The `_calculate_envelope_level()` method uses if-elif statements to determine the current stage, minimizing branching.

3. **Precomputed constants**: Values like the sustain level are precomputed and stored, rather than calculated on each update.

4. **Integer math**: The final duty cycle is converted to an integer, which is typically faster than floating-point operations on embedded systems.

5. **Asynchronous updates**: The `update()` method is asynchronous, allowing it to be called without blocking the main game loop.

While this implementation is efficient for the purposes of this game engine, there are potential optimizations that could be made for more demanding applications, such as using lookup tables for envelope shapes or implementing more complex envelope curves.




# Magnet Power-Up Analysis in Pong Game

## Table of Contents
1. [Introduction](#introduction)
2. [Power-Up Creation and Collection](#power-up-creation-and-collection)
3. [Paddle Implementation](#paddle-implementation)
4. [Ball Behavior Modification](#ball-behavior-modification)
5. [Physics Simulation](#physics-simulation)
6. [Visual and Audio Feedback](#visual-and-audio-feedback)
7. [Conclusion](#conclusion)

## Introduction

The magnet power-up in the Pong game introduces an interesting dynamic by allowing paddles to attract or repel the ball. This document explains how this power-up is implemented, its effects on game objects, and how it changes the gameplay.

## Power-Up Creation and Collection

The magnet power-up is created along with other power-ups in the `Pong` class:

```python
class Pong:
    def update_power_ups(self):
        if random.random() < 0.02:
            self.power_ups.append(PowerUp(random.randint(20, 220), random.randint(20, 115)))

class PowerUp:
    def __init__(self, x, y):
        self.type = random.choice(["grow", "shrink", "magnet", "control", "speed", "multiball"])
        self.color = {
            # ... other power-ups ...
            "magnet": colors.BLUE,
            # ... other power-ups ...
        }[self.type]
```

When a paddle collects the power-up:

```python
class Pong:
    async def update_power_ups(self):
        for power_up in self.power_ups[:]:
            if (abs(power_up.x - self.paddle1.x) < 10 and
                self.paddle1.y <= power_up.y <= self.paddle1.y + self.paddle1.height):
                self.apply_power_up(self.paddle1, power_up)
                # ... similar code for paddle2 ...

    def apply_power_up(self, paddle, power_up):
        paddle.apply_power_up(power_up.type)
        # ... other power-up effects ...
```

![Alt text](png/power_up_cretion_and_collection.png?raw=true "Title")

## Paddle Implementation

The `Paddle` class is modified to handle the magnet power-up:

```python
class Paddle:
    def __init__(self, x, y, width, height):
        # ... other initializations ...
        self.magnet_strength = 0

    def apply_power_up(self, power_up_type):
        self.power_up_type = power_up_type
        if power_up_type == "magnet":
            self.magnet_strength = random.choice([-0.5, 0.5])  # Negative for repel, positive for attract
        # ... handle other power-ups ...
        self.power_up_timer = 300  # Power-up lasts for 300 frames (5 seconds)

    def update(self):
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
            if self.power_up_timer == 0:
                # ... reset other power-ups ...
                self.magnet_strength = 0
```

## Ball Behavior Modification

The `Ball` class is updated to account for the magnetic effect:

```python
class Ball:
    def move(self, paddles):
        self.x += self.vx
        self.y += self.vy

        # Apply magnet effect
        for paddle in paddles:
            if paddle.power_up_type == "magnet":
                dx = paddle.x - self.x
                dy = (paddle.y + paddle.height / 2) - self.y
                distance = (dx**2 + dy**2)**0.5
                if distance < 50:  # Magnet effect range
                    force = paddle.magnet_strength / (distance**2)
                    self.vx += force * dx / distance
                    self.vy += force * dy / distance
```

![Alt text](png/ball_behavior_modification.png?raw=true "Title")

## Physics Simulation

The magnetic effect is simulated using an inverse square law, similar to real magnetic fields:

1. The force is proportional to $\frac{1}{r^2}$, where $r$ is the distance between the ball and paddle.
2. The direction of the force is along the line connecting the ball and paddle center.
3. The magnitude of the force is scaled by the `magnet_strength` parameter.

The resulting acceleration is added to the ball's velocity:

```python
force = paddle.magnet_strength / (distance**2)
self.vx += force * dx / distance
self.vy += force * dy / distance
```

This creates a more realistic and dynamic magnetic effect, where the influence becomes stronger as the ball gets closer to the paddle.

## Visual and Audio Feedback

Visual feedback for the magnet power-up is provided through the paddle color and a text indicator:

```python
class Paddle:
    def draw(self, lcd):
        if self.power_up_type == "magnet":
            color = colors.BLUE
        # ... handle other power-up colors ...

class Pong:
    def draw(self, lcd):
        # ... other drawing code ...
        if self.paddle1.power_up_type:
            lcd.text(self.paddle1.power_up_type.upper(), 5, 125, colors.WHITE)
        if self.paddle2.power_up_type:
            lcd.text(self.paddle2.power_up_type.upper(), 185, 125, colors.WHITE)
```

Audio feedback is provided when the power-up is collected:

```python
class Pong:
    async def update_power_ups(self):
        # ... power-up collection code ...
        self.audio_engine.play_power_up_collect()

class AudioEngine:
    def play_power_up_collect(self):
        powerup_sound = SawtoothWave(0)
        powerup_sound.set_frequency(880)  # A5 note
        powerup_sound.attack = 0.01
        powerup_sound.decay = 0.1
        powerup_sound.sustain = 0.3
        powerup_sound.release = 0.2
        self.add_sound_generator(powerup_sound)
        powerup_sound.note_on(timeout=0.3)  # 300ms sound
```

## Conclusion

The magnet power-up adds an interesting dynamic to the Pong game by introducing a new force that affects the ball's movement. Here's a summary of its implementation and effects:

1. The power-up is randomly generated and can be collected by paddles.
2. When active, it gives the paddle a magnetic property that can attract or repel the ball.
3. The magnetic effect is simulated using an inverse square law, creating a realistic force field.
4. Visual feedback is provided through paddle color changes and text indicators.
5. Audio feedback is given when the power-up is collected.

This power-up adds depth to the gameplay, allowing for more strategic play and unexpected ball trajectories, enhancing the overall gaming experience.

![Alt text](png/power_up_conclusion.png?raw=true "Title")

This diagram illustrates how the magnet power-up integrates into the overall game system, affecting multiple components and ultimately enhancing the player experience through new gameplay dynamics and feedback mechanisms.