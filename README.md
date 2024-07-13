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