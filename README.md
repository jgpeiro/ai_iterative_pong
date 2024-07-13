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