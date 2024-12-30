import pygame
import time
import random
import math
from PIL import Image, ImageDraw, ImageFilter
import os
import psutil  # For CPU temperature

# Initialize Pygame
pygame.init()

# Screen dimensions (smaller to save resources)
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyBench")

# Font for FPS display
font = pygame.font.Font(None, 36)

# Global variables for FPS counter
fps = 0
frame_count = 0
last_time = time.time()

# Disk class to represent each moving disk with Gaussian blur
class Disk:
    def __init__(self):
        self.radius = random.randint(20, 50)  # Random size for the disk
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.x_speed = random.randint(-3, 3)
        self.y_speed = random.randint(-3, 3)
        
        # Create the blurred disk image
        self.image = self.create_blurred_disk()
        self.image_surface = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
    
    def create_blurred_disk(self):
        # Create the disk image with normal resolution
        disk_image = Image.new('RGB', (self.radius * 2, self.radius * 2), (255, 255, 255))  # White background
        draw = ImageDraw.Draw(disk_image)
        
        # Draw the disk (ellipse)
        draw.ellipse([0, 0, self.radius * 2, self.radius * 2], fill=self.color)
        
        # Apply Gaussian Blur using Pillow
        blurred_image = disk_image.filter(ImageFilter.GaussianBlur(radius=5))  # Apply Gaussian blur to disk
        
        return blurred_image

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
        # Bounce off the walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.x_speed *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.y_speed *= -1

    def draw(self, screen):
        screen.blit(self.image_surface, (self.x - self.radius, self.y - self.radius))  # Blit the blurred image


# Function to generate a random 2D disk and apply Gaussian blur using Pillow
def generate_image():
    image = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))  # White background
    draw = ImageDraw.Draw(image)
    
    # Random color for the disk
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Random radius and center for the disk
    radius = random.randint(50, 150)  # Reduced radius for a smaller image
    center = (random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius))
    
    # Draw the disk (ellipse)
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], fill=color)
    
    # Apply Gaussian Blur using Pillow
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
    
    return blurred_image

# Function to perform a variety of intensive floating-point operations
def intensive_floating_point_benchmark(num_iterations=100000):
    total_calculations = 0
    
    # 1. Trigonometric Calculations (Sine and Cosine)
    result = 0.0
    for i in range(num_iterations):
        result += math.sin(i * 0.1) * math.cos(i * 0.1)
        total_calculations += 1
    
    # 2. Exponentiation and Logarithms
    for i in range(num_iterations):
        result += math.exp(i * 0.001) * math.log(i + 1)
        total_calculations += 1

    # 3. Large Scale Summation with Random Floating Point Numbers
    random_values = [random.random() for _ in range(50000)]  # Reduced number of random values
    sum_of_values = sum(random_values)
    total_calculations += len(random_values)
    
    return total_calculations, result, sum_of_values

# Function to perform disk benchmark
def disk_benchmark(file_count=0):
    file_path = f"test_benchmark_file_{file_count}.tmp"
    
    # Write test
    with open(file_path, "wb") as f:
        start_time = time.time()
        f.write(os.urandom(1024 * 1024 * 30))  # Write 30 MB of random data
        write_time = time.time() - start_time
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # File size in MB
    
    # Read test
    with open(file_path, "rb") as f:
        start_time = time.time()
        data = f.read()
        read_time = time.time() - start_time
    
    os.remove(file_path)  # Clean up
    
    return write_time, read_time, file_size

# Function to update FPS and display benchmark results
def update_benchmark():
    global fps, frame_count, last_time, floating_point_calculations, disk_file_count
    
    # Calculate FPS
    frame_count += 1
    current_time = time.time()
    elapsed_time = current_time - last_time
    if elapsed_time >= 1.0:
        fps = frame_count / elapsed_time
        frame_count = 0
        last_time = current_time
    
    # Perform intensive floating point benchmark
    floating_point_calculations, result, sum_of_values = intensive_floating_point_benchmark()
    
    # Perform disk benchmark
    write_time, read_time, file_size = disk_benchmark(disk_file_count)
    disk_file_count += 1
    
    # Get CPU temperature
    cpu_temp = get_cpu_temperature()
    
    return fps, write_time, read_time, file_size, floating_point_calculations, cpu_temp

# Function to get CPU temperature
def get_cpu_temperature():
    try:
        # Attempt to fetch CPU temperature using psutil
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                if name.startswith("core"):
                    return entry.current
    except Exception as e:
        return None  # If unable to fetch the temperature

# Main loop for the Pygame window
running = True
clock = pygame.time.Clock()

# Disk management variables
disks = []
max_disks = 550  # Number of disks
disks_spawned_per_second = 15  # Increase the spawning rate of disks
disks_deleted_per_second = 6  # Deleting 6 disks per second
disk_delete_timer = time.time()
disk_spawn_timer = time.time()
disk_spawning_complete = False

# Image generation for display
image = generate_image()
image_surface = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

# Disk file counter
disk_file_count = 0

# Main loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn disks if not yet completed
    if not disk_spawning_complete and len(disks) < max_disks:
        current_time = time.time()
        if current_time - disk_spawn_timer >= 1.0 / disks_spawned_per_second:
            disks.append(Disk())  # Add a new disk
            disk_spawn_timer = current_time  # Reset the spawn timer

    elif len(disks) == max_disks:
        disk_spawning_complete = True  # Stop spawning after max disks

    # Update disk list: move disks and delete 3 per second
    if disk_spawning_complete:
        current_time = time.time()
        for disk in disks:
            disk.move()

        if current_time - disk_delete_timer >= 1.0:  # Delete 3 disks every second
            disks = disks[disks_deleted_per_second:]  # Remove the first 3 disks
            disk_delete_timer = current_time

        if len(disks) == 0:
            # Reset the process once all disks are deleted
            disk_spawning_complete = False  # Restart the spawning process

    # Update the benchmark and FPS counter
    fps, write_time, read_time, file_size, floating_point_calculations, cpu_temp = update_benchmark()

    # Relay FPS, number of disks, floating point calculations, file size, and number of tests to the console (command prompt)
    cpu_temp_display = f"{cpu_temp:.2f}°C" if cpu_temp else "N/A"
    print(f"FPS: {fps:.2f} | Number of Disks: {len(disks)} | Floating Point Calculations: {floating_point_calculations} | "
          f"Disk Write: {write_time:.4f}s | Disk Read: {read_time:.4f}s | File Size: {file_size:.2f} MB | CPU Temp: {cpu_temp_display}")

    # Clear the screen
    screen.fill((0, 0, 0))

    # Display FPS
    fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    # Display Disk write and read times
    disk_text = font.render(f"Disk Write: {write_time:.4f}s | Disk Read: {read_time:.4f}s", True, (255, 255, 255))
    screen.blit(disk_text, (10, 50))

    # Display the image with Gaussian blur
    screen.blit(image_surface, (WIDTH // 2 - image.width // 2, HEIGHT // 2 - image.height // 2))

    # Display the moving and blurred disks
    for disk in disks:
        disk.draw(screen)

    # Display CPU temperature
    cpu_temp_text = font.render(f"CPU Temp: {cpu_temp_display}", True, (255, 255, 255))
    screen.blit(cpu_temp_text, (10, 90))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
