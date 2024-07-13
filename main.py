import uasyncio as asyncio
import time
import machine
import random
import math
import gc
import st7789_fb

# Color definitions
class colors:
    BLACK = const(0x0000)
    WHITE = const(0xFFFF)
    RED = const(0xF800)
    GREEN = const(0x07E0)
    BLUE = const(0x001F)
    CYAN = const(0x07FF)
    MAGENTA = const(0xF81F)
    YELLOW = const(0xFFE0)
    ORANGE = const(0xFD20)
    INDIGO = const(0x4810)
    VIOLET = const(0x8010)

    @staticmethod
    def color_brightness(color, brightness):
        if brightness < 0 or brightness > 1:
            return color
        r = (color >> 11) & 0x1F
        g = (color >> 5) & 0x3F
        b = color & 0x1F
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        return (r << 11) | (g << 5) | b


class SevenSegmentDisplay:
    def __init__(self, x, y, digit_height):
        self.x = x
        self.y = y
        self.digit_height = digit_height
        self.digit_width = digit_height * 3 // 5 + 5
        self.segment_width = max(2, digit_height // 8)
        self.gap = max(1, digit_height // 16)
        self.segments = [
            [(1, 0), (4, 0)],  # Top
            [(4, 0), (4, 2)],  # Top right
            [(4, 2), (4, 4)],  # Bottom right
            [(1, 4), (4, 4)],  # Bottom
            [(0, 2), (0, 4)],  # Bottom left
            [(0, 0), (0, 2)],  # Top left
            [(1, 2), (4, 2)]   # Middle
        ]
        self.digit_map = {
            0: [1, 1, 1, 1, 1, 1, 0],
            1: [0, 1, 1, 0, 0, 0, 0],
            2: [1, 1, 0, 1, 1, 0, 1],
            3: [1, 1, 1, 1, 0, 0, 1],
            4: [0, 1, 1, 0, 0, 1, 1],
            5: [1, 0, 1, 1, 0, 1, 1],
            6: [1, 0, 1, 1, 1, 1, 1],
            7: [1, 1, 1, 0, 0, 0, 0],
            8: [1, 1, 1, 1, 1, 1, 1],
            9: [1, 1, 1, 1, 0, 1, 1]
        }

    def draw_digit(self, lcd, digit, color):
        segments = self.digit_map[digit]
        for i, segment in enumerate(self.segments):
            if segments[i]:
                start, end = segment
                sx = self.x + start[0] * self.digit_width // 5
                sy = self.y + start[1] * self.digit_height // 4
                ex = self.x + end[0] * self.digit_width // 5
                ey = self.y + end[1] * self.digit_height // 4
                if start[0] == end[0]:  # Vertical segment
                    lcd.fill_rect(sx, sy + self.gap, self.segment_width, ey - sy - 2*self.gap, color)
                else:  # Horizontal segment
                    lcd.fill_rect(sx + self.gap, sy, ex - sx - 2*self.gap, self.segment_width, color)

    def draw_number(self, lcd, number, color):
        original_x = self.x
        for digit in f"{number:06d}":
            self.draw_digit(lcd, int(digit), color)
            self.x += self.digit_width + self.gap
        self.x = original_x

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0
        self.acceleration = 0.5
        self.max_speed = 8
        self.friction = 0.9
        self.color = colors.WHITE
        self.power_up_timer = 0
        self.power_up_type = None
        self.rainbow_position = 0
        self.magnet_strength = 0

    def move(self, direction):
        if direction == "up":
            self.velocity -= self.acceleration
        elif direction == "down":
            self.velocity += self.acceleration
        
        self.velocity = max(-self.max_speed, min(self.max_speed, self.velocity))
        self.y += self.velocity
        self.y = max(0, min(135 - self.height, self.y))
        
        # Apply friction
        self.velocity *= self.friction

    def draw(self, lcd):
        if self.power_up_type == "rainbow":
            self.rainbow_position = (self.rainbow_position + 5) % 256
            color = colors.color_brightness(colors.CYAN, self.rainbow_position / 255)
        elif self.power_up_timer > 0:
            color = {
                "grow": colors.GREEN,
                "shrink": colors.RED,
                "magnet": colors.BLUE,
                "control": colors.YELLOW
            }.get(self.power_up_type, self.color)
        else:
            color = self.color

        # Draw rounded rectangle
        lcd.fill_rect(int(self.x), int(self.y) + 2, int(self.width), int(self.height) - 4, color)
        lcd.fill_rect(int(self.x) + 1, int(self.y) + 1, int(self.width) - 2, int(self.height) - 2, color)
        lcd.fill_rect(int(self.x) + 2, int(self.y), int(self.width) - 4, int(self.height), color)

    def apply_power_up(self, power_up_type):
        self.power_up_type = power_up_type
        if power_up_type == "grow":
            self.height = min(40, self.height + 10)
        elif power_up_type == "shrink":
            self.height = max(10, self.height - 5)
        elif power_up_type == "magnet":
            self.magnet_strength = random.choice([-0.5, 0.5])  # Negative for repel, positive for attract
        elif power_up_type == "control":
            pass  # Control is handled in the Ball class
        self.power_up_timer = 300  # Power-up lasts for 300 frames (5 seconds)

    def update(self):
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
            if self.power_up_timer == 0:
                self.height = 20  # Reset to default height
                self.power_up_type = None
                self.magnet_strength = 0

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = random.choice([-2, 2])
        self.vy = random.choice([-2, 2])
        self.max_speed = 6
        self.color = colors.WHITE
        self.controlled = False
        self.controlled_by = None

    def move(self, paddles):
        if self.controlled and self.controlled_by:
            # Move the ball with the controlling paddle
            self.y = self.controlled_by.y + self.controlled_by.height / 2
            if self.controlled_by.x < 120:  # Left paddle
                self.x = self.controlled_by.x + self.controlled_by.width + self.radius
            else:  # Right paddle
                self.x = self.controlled_by.x - self.radius
        else:
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

    def bounce(self, paddle_velocity):
        self.vx = -self.vx
        self.vy += paddle_velocity * 0.5
        
        speed = (self.vx**2 + self.vy**2)**0.5
        if speed < self.max_speed:
            factor = (speed + 0.2) / speed
            self.vx *= factor
            self.vy *= factor
        
        if speed > self.max_speed:
            factor = self.max_speed / speed
            self.vx *= factor
            self.vy *= factor

    def draw(self, lcd):
        lcd.fill_circle(int(self.x), int(self.y), self.radius, self.color)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.type = random.choice(["grow", "shrink", "magnet", "control", "speed", "multiball"])
        self.color = {
            "grow": colors.GREEN,
            "shrink": colors.RED,
            "magnet": colors.BLUE,
            "control": colors.YELLOW,
            "speed": colors.MAGENTA,
            "multiball": colors.CYAN
        }[self.type]
        self.letter = self.type[0].upper()

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > 240:
            self.vx = -self.vx
        if self.y < 0 or self.y > 135:
            self.vy = -self.vy

    def draw(self, lcd):
        lcd.fill_circle(int(self.x), int(self.y), self.radius, self.color)
        lcd.text(self.letter, int(self.x) - 3, int(self.y) - 3, colors.WHITE)

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, lcd):
        lcd.pixel(int(self.x), int(self.y), self.color)

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

    def update(self):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

    def draw(self, lcd):
        for particle in self.particles:
            particle.draw(lcd)


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
        
        self.start_freq = 440
        self.min_freq = 110
        
        self.current_time = 0
        self.is_note_on = False
        self.envelope_stage = 'off'
        self.timeout = 0  # New timeout attribute
    
    def set_frequency(self, freq):
        self.pwm.freq(int(freq))
    
    def set_volume(self, vol):
        self.volume = max(0, min(100, vol))
    
    def note_on(self, timeout=0.5):  # Default timeout of 0.5 seconds
        self.is_note_on = True
        self.envelope_stage = 'attack'
        self.current_time = 0
        self.timeout = timeout
    
    def note_off(self):
        self.is_note_on = False
        self.envelope_stage = 'release'
    
    async def update(self, dt):
        level = self._calculate_envelope_level()
        duty = int(level * self.volume * 655.35)  # Scale to 16-bit duty cycle
        self.pwm.duty_u16(duty)
        
        self.current_time += dt
        
        # Check for timeout
        if self.timeout > 0:
            self.timeout -= dt
            if self.timeout <= 0:
                self.note_off()
    
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

class SquareWave(SoundGenerator):
    def __init__(self, pin_number, duty_cycle=0.5):
        super().__init__(pin_number)
        self.duty_cycle = duty_cycle

class SawtoothWave(SoundGenerator):
    pass

class SineWave(SoundGenerator):
    pass

class NoiseGenerator(SoundGenerator):
    pass

class AudioEngine:
    def __init__(self):
        self.sound_generators = []
    
    def add_sound_generator(self, generator):
        if len(self.sound_generators) < 8:
            self.sound_generators.append(generator)
    
    async def update(self, dt):
        for generator in self.sound_generators:
            await generator.update(dt)
    
    def remove_inactive_generators(self):
        self.sound_generators = [gen for gen in self.sound_generators if gen.envelope_stage != 'off']

    def play_paddle_hit(self):
        hit_sound = SquareWave(0)  # Assuming PWM pin 14 for audio
        hit_sound.set_frequency(660)  # E5 note
        hit_sound.attack = 0.01
        hit_sound.decay = 0.05
        hit_sound.sustain = 0.2
        hit_sound.release = 0.1
        self.add_sound_generator(hit_sound)
        hit_sound.note_on(timeout=0.2)  # 200ms sound

    def play_wall_bounce(self):
        bounce_sound = SineWave(0)
        bounce_sound.set_frequency(440)  # A4 note
        bounce_sound.attack = 0.01
        bounce_sound.decay = 0.05
        bounce_sound.sustain = 0.1
        bounce_sound.release = 0.1
        self.add_sound_generator(bounce_sound)
        bounce_sound.note_on(timeout=0.15)  # 150ms sound

    def play_power_up_collect(self):
        powerup_sound = SawtoothWave(0)
        powerup_sound.set_frequency(880)  # A5 note
        powerup_sound.attack = 0.01
        powerup_sound.decay = 0.1
        powerup_sound.sustain = 0.3
        powerup_sound.release = 0.2
        self.add_sound_generator(powerup_sound)
        powerup_sound.note_on(timeout=0.3)  # 300ms sound

    def play_goal(self):
        goal_sound = NoiseGenerator(0)
        goal_sound.set_frequency(220)  # A3 note
        goal_sound.attack = 0.01
        goal_sound.decay = 0.3
        goal_sound.sustain = 0.5
        goal_sound.release = 0.5
        self.add_sound_generator(goal_sound)
        goal_sound.note_on(timeout=1.0)  # 1 second sound

class Pong:
    def __init__(self):
        self.paddle1 = Paddle(10, 60, 5, 20)
        self.paddle2 = Paddle(225, 60, 5, 20)
        self.balls = [Ball(120, 67, 3)]
        self.score1 = 0
        self.score2 = 0
        self.running = True
        self.debug = False
        self.last_time = time.ticks_ms()
        self.frame_count = 0
        self.fps = 0
        self.particle_system = ParticleSystem()
        self.goal_animation = None
        self.rainbow_colors = [colors.RED, colors.ORANGE, colors.YELLOW, colors.GREEN, colors.BLUE, colors.INDIGO, colors.VIOLET]
        self.power_ups = []
        self.instruction_scroll = 0
        self.instruction_velocity = 0
        self.last_button_press_time = 0
        self.game_state = "welcome"
        self.score_display1 = SevenSegmentDisplay(10, 5, 16)
        self.score_display2 = SevenSegmentDisplay(140, 5, 16)
        self.return_to_welcome_cooldown = 0
        self.score_color = colors.CYAN
        self.ai_difficulty = "medium"
        self.paused = False
        self.audio_engine = AudioEngine()
    
    def update_goal(self, event):
        self.goal_animation['frame'] += 1
        if self.goal_animation['frame'] >= 30:  # Extended goal animation time
            self.goal_animation = None
            self.game_state = "playing"
            for generator in self.audio_engine.sound_generators:
                generator.note_off()
            self.reset_ball()
            self.paddle1 = Paddle(10, 60, 5, 20)  # Reset paddles
            self.paddle2 = Paddle(225, 60, 5, 20)

    def update_paused(self, event):
        if event == "A":
            self.paused = False
            self.game_state = "playing"
        elif event == "B":
            self.game_state = "welcome"
            self.instruction_scroll = 0
            self.instruction_velocity = 0
            self.return_to_welcome_cooldown = 30
        elif event == "U":
            self.ai_difficulty = "hard" if self.ai_difficulty == "medium" else "medium"
        elif event == "D":
            self.ai_difficulty = "easy" if self.ai_difficulty == "medium" else "medium"

    def start_goal_animation(self, is_left_goal):
        self.game_state = "goal"
        self.goal_animation = {
            'duration': 180,
            'frame': 0,
            'is_left_goal': is_left_goal
        }
        for _ in range(50):  # More particles for goal celebration
            self.particle_system.add_particle(
                random.randint(0, 240), random.randint(0, 135),
                random.uniform(-2, 2), random.uniform(-2, 2),
                random.choice(self.rainbow_colors),
                random.randint(30, 90)
            )
    
    def update_ai(self):
        if self.balls:
            target_ball = min(self.balls, key=lambda b: abs(b.y - (self.paddle2.y + self.paddle2.height / 2)))
            target_y = target_ball.y - self.paddle2.height / 2
            
            if self.ai_difficulty == "easy":
                speed_factor = 0.5
            elif self.ai_difficulty == "medium":
                speed_factor = 0.75
            else:  # hard
                speed_factor = 1.0
            
            if self.paddle2.y < target_y:
                self.paddle2.move("down")
                self.paddle2.velocity *= speed_factor
            elif self.paddle2.y > target_y:
                self.paddle2.move("up")
                self.paddle2.velocity *= speed_factor
        
    def reset_game(self):
        self.score1 = 0
        self.score2 = 0
        self.reset_ball()
        self.paddle1 = Paddle(10, 60, 5, 20)
        self.paddle2 = Paddle(225, 60, 5, 20)
        self.power_ups = []
        self.balls = [Ball(120, 67, 3)]
    
    def reset_ball(self):
        self.balls = [Ball(120, 67, 3)]
    
    def show_instructions(self, lcd):
        lcd.fill(0)
        instructions = [
            "Welcome to Pong!",
            "",
            "Game Controls:",
            "Player 1: Joy Up/Down",
            "Player 2/AI: A/B buttons",
            "",
            "Game Elements:",
            "- Paddles: Control with",
            "  the above buttons",
            "- Ball: Bounces between",
            "  paddles",
            "- Power-ups: Collect to",
            "  grow, shrink, change",
            "  color, speed up, or",
            "  add multiple balls",
            "",
            "Scoring:",
            "- Score increases with",
            "  paddle movement and",
            "  interactions",
            "- Goals worth millions",
            "",
            "Special Controls:",
            "- Hold A+B: Toggle debug",
            "- Hold Joy Center (2s):",
            "  Pause game",
            "- In pause menu:",
            "  - A: Resume",
            "  - B: Return to main menu",
            "  - Up/Down: Change AI",
            "    difficulty",
            "",
            "Press any button to start",
            "Scroll with Joy Up/Down"
        ]
        y_offset = -self.instruction_scroll
        for i, line in enumerate(instructions):
            y = 10 + i * 20 + y_offset
            if 0 <= y < 135:
                lcd.text(line, 10, int(y), colors.WHITE)

        # Add particles for visual effect
        if random.random() < 0.1:
            self.particle_system.add_particle(
                random.randint(0, 240), 135,
                random.uniform(-1, 1), random.uniform(-3, -1),
                random.choice(self.rainbow_colors),
                random.randint(30, 90)
            )
    
    def update_welcome(self, event):
        # Smooth scrolling with minimal acceleration
        if event == "U":
            self.instruction_velocity -= 0.5
        elif event == "D":
            self.instruction_velocity += 0.5
        else:
            self.instruction_velocity *= 0.9  # Deceleration

        self.instruction_velocity = max(-5, min(5, self.instruction_velocity))
        self.instruction_scroll += self.instruction_velocity
        self.instruction_scroll = max(0, min(300, self.instruction_scroll))

        if event and event not in ["U", "D"] and self.return_to_welcome_cooldown == 0:
            self.game_state = "playing"
            self.reset_game()
            
    async def update(self, event):
        if self.game_state == "welcome":
            self.update_welcome(event)
        elif self.game_state == "playing":
            await self.update_playing(event)
        elif self.game_state == "goal":
            self.update_goal(event)
        elif self.game_state == "paused":
            self.update_paused(event)

        # Update particles
        self.particle_system.update()

        # FPS calculation
        self.frame_count += 1
        if self.frame_count == 30:
            current_time = time.ticks_ms()
            self.fps = 30000 / (current_time - self.last_time)
            self.last_time = current_time
            self.frame_count = 0

        # Update return to welcome cooldown
        if self.return_to_welcome_cooldown > 0:
            self.return_to_welcome_cooldown -= 1

        # Update audio engine
        await self.audio_engine.update(0.01)  # 10ms update interval
        self.audio_engine.remove_inactive_generators()

    async def update_playing(self, event):
        if event == "U":
            self.paddle1.move("up")
            self.score1 += 10  # Score for paddle movement
        elif event == "D":
            self.paddle1.move("down")
            self.score1 += 10  # Score for paddle movement
        elif event == "A":
            self.paddle2.move("up")
            self.score2 += 10  # Score for paddle movement
        elif event == "B":
            self.paddle2.move("down")
            self.score2 += 10  # Score for paddle movement
        elif event == "C":
            self.paused = True
            self.game_state = "paused"
        
        self.paddle1.move(None)
        self.paddle2.move(None)
        self.paddle1.update()
        self.paddle2.update()

        self.update_ai()

        for ball in self.balls:
            ball.move([self.paddle1, self.paddle2])

            if ball.y - ball.radius <= 0 or ball.y + ball.radius >= 135:
                ball.vy = -ball.vy
                self.audio_engine.play_wall_bounce()

            if (ball.x - ball.radius <= self.paddle1.x + self.paddle1.width and
                self.paddle1.y <= ball.y <= self.paddle1.y + self.paddle1.height):
                if self.paddle1.power_up_type == "control":
                    ball.controlled = True
                    ball.controlled_by = self.paddle1
                else:
                    ball.bounce(self.paddle1.velocity)
                self.score1 += 100  # Score for ball hit
                self.add_hit_particles(ball.x, ball.y)
                self.audio_engine.play_paddle_hit()
            elif (ball.x + ball.radius >= self.paddle2.x and
                  self.paddle2.y <= ball.y <= self.paddle2.y + self.paddle2.height):
                if self.paddle2.power_up_type == "control":
                    ball.controlled = True
                    ball.controlled_by = self.paddle2
                else:
                    ball.bounce(self.paddle2.velocity)
                self.score2 += 100  # Score for ball hit
                self.add_hit_particles(ball.x, ball.y)
                self.audio_engine.play_paddle_hit()

        # Check for goals
        for ball in self.balls[:]:
            if ball.x < 0:
                self.score2 += 10_000  # Score for goal
                self.balls.remove(ball)
                self.start_goal_animation(is_left_goal=True)
                self.audio_engine.play_goal()
            elif ball.x > 240:
                self.score1 += 10_000  # Score for goal
                self.balls.remove(ball)
                self.start_goal_animation(is_left_goal=False)
                self.audio_engine.play_goal()

        if not self.balls:
            self.reset_ball()

        await self.update_power_ups()

        # Cap scores at 999999
        self.score1 = min(999999, self.score1)
        self.score2 = min(999999, self.score2)

    async def update_power_ups(self):
        if random.random() < 0.02:
            self.power_ups.append(PowerUp(random.randint(20, 220), random.randint(20, 115)))

        for power_up in self.power_ups:
            power_up.move()

        for power_up in self.power_ups[:]:
            if (abs(power_up.x - self.paddle1.x) < 10 and
                self.paddle1.y <= power_up.y <= self.paddle1.y + self.paddle1.height):
                self.apply_power_up(self.paddle1, power_up)
                self.score1 += 1000  # Score for power-up collection
                self.power_ups.remove(power_up)
                self.audio_engine.play_power_up_collect()
            elif (abs(power_up.x - self.paddle2.x) < 10 and
                  self.paddle2.y <= power_up.y <= self.paddle2.y + self.paddle2.height):
                self.apply_power_up(self.paddle2, power_up)
                self.score2 += 1000  # Score for power-up collection
                self.power_ups.remove(power_up)
                self.audio_engine.play_power_up_collect()

        self.power_ups = [pu for pu in self.power_ups if 0 <= pu.x <= 240 and 0 <= pu.y <= 135]

    def apply_power_up(self, paddle, power_up):
        paddle.apply_power_up(power_up.type)
        if power_up.type == "speed":
            for ball in self.balls:
                ball.max_speed *= 1.5
        elif power_up.type == "multiball":
            new_ball = Ball(120, 67, 3)
            new_ball.vx = -self.balls[0].vx
            new_ball.vy = -self.balls[0].vy
            self.balls.append(new_ball)

    def add_hit_particles(self, x, y):
        for _ in range(10):
            self.particle_system.add_particle(
                x, y,
                random.uniform(-2, 2), random.uniform(-2, 2),
                random.choice([colors.WHITE, colors.CYAN, colors.YELLOW]),
                random.randint(15, 30)
            )

    def draw(self, lcd):
        lcd.fill(0)
        if self.game_state == "welcome":
            self.show_instructions(lcd)
        elif self.game_state == "playing":
            self.draw_game(lcd)
        elif self.game_state == "goal":
            self.draw_goal_animation(lcd)
        elif self.game_state == "paused":
            self.draw_pause_menu(lcd)

        self.particle_system.draw(lcd)

        # Draw the score only in the playing state
        if self.game_state == "playing":
            self.score_display1.draw_number(lcd, self.score1, self.score_color)
            self.score_display2.draw_number(lcd, self.score2, self.score_color)

        # Draw active power-up names
        if self.paddle1.power_up_type:
            lcd.text(self.paddle1.power_up_type.upper(), 5, 125, colors.WHITE)
        if self.paddle2.power_up_type:
            lcd.text(self.paddle2.power_up_type.upper(), 185, 125, colors.WHITE)

        if self.debug:
            lcd.text(f"FPS: {self.fps:.1f}", 5, 20, colors.YELLOW)
            lcd.text(f"MEM: {gc.mem_free()} B", 5, 30, colors.YELLOW)
            lcd.text(f"CPU: {100 * machine.freq() / 1000000:.1f}%", 5, 40, colors.YELLOW)

    def draw_game(self, lcd):
        self.paddle1.draw(lcd)
        self.paddle2.draw(lcd)
        for ball in self.balls:
            ball.draw(lcd)
        
        for power_up in self.power_ups:
            power_up.draw(lcd)

    def draw_goal_animation(self, lcd):
        # Draw the "GOAL!" text
        text = "GOAL!"
        text_width = len(text) * 8
        x = (240 - text_width) // 2
        y = 50

        for i, char in enumerate(text):
            color_index = (i + self.goal_animation['frame'] // 5) % len(self.rainbow_colors)
            color = self.rainbow_colors[color_index]
            lcd.text(char, x + i * 8, y, color)

        # Draw expanding circles
        radius = min(100, self.goal_animation['frame'] * 2)
        lcd.circle(120, 67, radius, colors.color_brightness(colors.WHITE, 1 - radius / 100))

        # Draw game objects
        self.paddle1.draw(lcd)
        self.paddle2.draw(lcd)
        for ball in self.balls:
            ball.draw(lcd)
        for power_up in self.power_ups:
            power_up.draw(lcd)

    def draw_pause_menu(self, lcd):
        lcd.fill_rect(60, 30, 120, 75, colors.BLUE)
        lcd.rect(60, 30, 120, 75, colors.WHITE)
        lcd.text("PAUSED", 95, 40, colors.WHITE)
        lcd.text("A: Resume", 70, 60, colors.WHITE)
        lcd.text("B: Main Menu", 70, 75, colors.WHITE)
        lcd.text(f"AI: {self.ai_difficulty}", 70, 90, colors.WHITE)

    def is_running(self):
        return self.running


# Hardware setup
sw_a = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
sw_b = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
joy_u = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
joy_d = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
joy_l = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
joy_r = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
joy_c = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
bl = machine.Pin(13, machine.Pin.OUT)
bl.value(1)

async def main():
    lcd = st7789_fb.LCD()
    pong = Pong()
    lcd.show()
    
    while pong.is_running():
        if sw_a.value() == 0 and sw_b.value() == 0:
            pong.debug = not pong.debug
        
        if sw_a.value() == 0:
            event = "A"
        elif sw_b.value() == 0:
            event = "B"
        elif joy_u.value() == 0:
            event = "U"
        elif joy_d.value() == 0:
            event = "D"
        elif joy_l.value() == 0:
            event = "L"
        elif joy_r.value() == 0:
            event = "R"
        elif joy_c.value() == 0:
            event = "C"
        else:
            event = ""
        
        await pong.update(event)
        pong.draw(lcd)
        lcd.show()
        
        await asyncio.sleep_ms(10)

if __name__ == "__main__":
    asyncio.run(main())

print("done")




