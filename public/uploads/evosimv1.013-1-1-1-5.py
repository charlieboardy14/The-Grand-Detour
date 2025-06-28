import random
import pygame
import sys
import math
import json # For settings import/export
import base64 # For settings import/export

# --------------------------
# Colors and Constants
# --------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
SATURATED_DIRT_BROWN = (120, 80, 40)
STONE_GRAY = (100, 100, 100)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (200, 200, 200)
GREEN_MEAT_COLOR = (0, 255, 0)
RED_MEAT_COLOR = (200, 0, 0)
ENERGY_BAR_BACKGROUND = BLACK
ENERGY_HIGH_COLOR = (0, 255, 0)
ENERGY_MID_COLOR = (255, 255, 0)
ENERGY_LOW_COLOR = (255, 0, 0)
ATTACK_LINE_COLOR = (255, 50, 50, 150) 
PLANT_INDICATOR_COLOR = (34, 139, 34) 
MENU_BUTTON_COLOR = (220, 220, 220)
MENU_BUTTON_BORDER_COLOR = (100, 100, 100)
MENU_BUTTON_HOVER_COLOR = (200, 200, 255)
MENU_TEXT_COLOR = BLACK

CELL_SIZE = 10 

INTENT_COLORS = {
    "idle": (150,150,150),"wandering":(180,180,180),"hunting":(255,165,0),
    "scavenging":(0,128,0),"attacking":(255,0,0),"rooting":PLANT_INDICATOR_COLOR, 
    "stationary":(50,50,50),"fleeing":(0,191,255), "active_movement": (100,100,255) # Light Blue for active movement
}
INTENT_INDICATOR_RADIUS = 3 

# Game States
STATE_MAIN_MENU = "main_menu"
STATE_PRE_GAME_SETTINGS = "pre_game_settings"
STATE_SIMULATION = "simulation"
STATE_IN_GAME_SETTINGS_MENU = "in_game_settings_menu"


# --------------------------
# Global Editable Settings
# --------------------------
SETTINGS = {
    # Display settings
    "screen_width":1200,"screen_height":650, 
    "world_width":8000,"world_height":6000, 
    "fps":300, 

    # Population settings
    "population_size":125, 
    "overcrowding_limit":5, 

    # Energy settings
    "initial_energy_min":300,"initial_energy_max":1500, 
    "energy_gain_meat":100,
    "movement_cost_rate_per_velocity": 1.25, 
    "cell_maintenance_costs":{ 
        "movement":0.01,"consumption":0.02,"luminescence":0.6,"roots":26, 
        "energy_processor":0.1,"eyes":0.02,"brain":0.06,"bone":0.1, 
        "unspecialized":0.6,"turn":0.6,"attack":0.05,
    },
    "base_maintenance_cost":0.22, 

    # Plant specific
    "plant_energy_absorption_rate_per_cell_per_second": 15.0, 


    # Reproduction & Genetics
    "reproduction_energy_ratio":0.8, 
    "reproduction_cooldown":2000, 
    "mutation_rate_default":0.03, 
    "max_energy_mutation_range":(-50,50), 
    "reproduction_cooldown_mutation_range":(-1000,1000), 
    "mutation_rate_mutation_range":(-0.01,0.01), 
    "child_energy_split_ratio":0.5, 
    "genetic_max_energy_min":100,"genetic_max_energy_max":3000,
    
    "initial_reproduction_distance_min": CELL_SIZE * 3,
    "initial_reproduction_distance_max": CELL_SIZE * 10,
    "reproduction_distance_mutation_range": (-CELL_SIZE * 0.5, CELL_SIZE * 0.5), 
    "min_reproduction_distance": CELL_SIZE * 1.5, 
    "max_reproduction_distance": CELL_SIZE * 20,  

    # Attack System
    "energy_drain_per_attack_cell_per_second":25.0, 
    "attack_energy_gain_ratio":0.6, 
    "attack_maintenance_cost_per_second":0.3, 
    "attack_range_bonus":CELL_SIZE*1.5, 

    # Meat settings
    "meat_energy_value":5,"green_meat_energy_value":10, 
    "meat_decay_time":60000, 
    "max_total_meat_items": 750, 
    "meat_lod_min_pixel_size": 1.5, 

    # Green Meat natural spawn settings
    "green_meat_spawn_interval":4000, 
    "green_meat_cluster_min_size":1,
    "green_meat_cluster_max_size":10, 
    "green_meat_cluster_radius":50,

    # Zoom and Camera
    "zoom_initial":1.0,"zoom_min":0.05,"zoom_max":5.0, 
    "zoom_step":0.1,"pinch_zoom_sensitivity":0.005, 
    
    # Slider for time rate
    "time_slider_rect":pygame.Rect(10,60,200,20), 
    "time_slider_min":0.0,"time_slider_max":5.0, 
    "default_time_rate":1.0,

    # Spatial Grid
    "spatial_grid_cell_size":200,
    "lineage_id_mutation_chance":0.001,
    "min_initial_spawn_separation": CELL_SIZE * 10,
    "target_search_cooldown_min_ms": 200, 
    "target_search_cooldown_max_ms": 600,
    "sporadic_move_cooldown_min_ms": 500, 
    "sporadic_move_cooldown_max_ms": 1500,
    "species_ui_zoom_threshold": 0.4, 
    "terrain_chunk_size": 32,
    "ai_update_stagger_factor": 5,

    # Cinematic Mode
    "cinematic_mode_default_on": False, 
    "cinematic_mode_target_zoom": 1.5, 
    "cinematic_camera_lerp_speed": 0.03, 
    "cinematic_event_lifetime_ms": 10000, 
    "cinematic_focus_duration_ms": 5000, 
    "cinematic_pan_duration_ms": 8000, 
    "cinematic_event_interest_scores": { 
        "attack": 10, "consume_meat": 5, "reproduce": 2, "die": 1, "active_movement": 4 
    }
}

SETTINGS_CATEGORIES = {
    "Display": ["screen_width", "screen_height", "world_width", "world_height", "fps"],
    "Population": ["population_size", "overcrowding_limit", "min_initial_spawn_separation"],
    "Energy & Costs": ["initial_energy_min", "initial_energy_max", "energy_gain_meat", 
                       "movement_cost_rate_per_velocity", "base_maintenance_cost", 
                       "plant_energy_absorption_rate_per_cell_per_second"],
    "Reproduction": ["reproduction_energy_ratio", "reproduction_cooldown", "child_energy_split_ratio",
                     "initial_reproduction_distance_min", "initial_reproduction_distance_max",
                     "min_reproduction_distance", "max_reproduction_distance"],
    "Genetics & Mutation": ["mutation_rate_default", "max_energy_mutation_range", 
                            "reproduction_cooldown_mutation_range", "mutation_rate_mutation_range",
                            "reproduction_distance_mutation_range", "lineage_id_mutation_chance",
                            "genetic_max_energy_min", "genetic_max_energy_max"],
    "Attack System": ["energy_drain_per_attack_cell_per_second", "attack_energy_gain_ratio",
                      "attack_maintenance_cost_per_second", "attack_range_bonus"],
    "Meat & Spawning": ["meat_energy_value", "green_meat_energy_value", "meat_decay_time", 
                        "max_total_meat_items", "green_meat_spawn_interval", 
                        "green_meat_cluster_min_size", "green_meat_cluster_max_size", "green_meat_cluster_radius"],
    "Camera & UI": ["zoom_initial", "zoom_min", "zoom_max", "zoom_step", "pinch_zoom_sensitivity",
                    "species_ui_zoom_threshold", "meat_lod_min_pixel_size"],
    "Simulation Speed & AI": ["default_time_rate", "time_slider_min", "time_slider_max", 
                              "target_search_cooldown_min_ms", "target_search_cooldown_max_ms",
                              "sporadic_move_cooldown_min_ms", "sporadic_move_cooldown_max_ms",
                              "ai_update_stagger_factor"],
    "Cinematic Mode": ["cinematic_mode_default_on", "cinematic_mode_target_zoom", 
                       "cinematic_camera_lerp_speed", "cinematic_event_lifetime_ms",
                       "cinematic_focus_duration_ms", "cinematic_pan_duration_ms"] 
}


CELL_COLORS = {
    "movement":(0,0,255),"consumption":(255,0,0),"luminescence":(255,255,0),"roots":BROWN,
    "energy_processor":(0,255,0),"eyes":(255,165,0),"brain":(75,0,130),"bone":(169,169,169),
    "unspecialized":(200,200,200),"pheromones":(0,255,255),"attack":(255,0,255),
}

# -------------------------- Helper Functions --------------------------
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def random_mutation(value, mutation_range, mutation_rate):
    if random.random() < mutation_rate:
        if isinstance(mutation_range, tuple) and len(mutation_range) == 2:
            return value + random.uniform(mutation_range[0], mutation_range[1])
        elif isinstance(mutation_range, (int, float)): 
             return value + random.uniform(-mutation_range, mutation_range)
    return value

def generate_unique_id():
    return random.getrandbits(32) 

# -------------------------- Terrain Generation --------------------------
def generate_terrain(world_width, world_height, terrain_cell_size):
    grid_width = world_width // terrain_cell_size
    grid_height = world_height // terrain_cell_size
    terrain_grid = [["dirt" for _ in range(grid_width)] for _ in range(grid_height)]
    
    total_terrain_cells = grid_width * grid_height
    stone_cells_count = total_terrain_cells // 7
    stone_positions = random.sample(range(total_terrain_cells), stone_cells_count)

    for pos_index in stone_positions:
        col = pos_index % grid_width
        row = pos_index // grid_width
        terrain_grid[row][col] = "stone"

    for _ in range(total_terrain_cells // 100): 
        cluster_center_col = random.randint(0, grid_width - 1)
        cluster_center_row = random.randint(0, grid_height - 1)
        if terrain_grid[cluster_center_row][cluster_center_col] == "stone":
            for _ in range(random.randint(5, 15)): 
                dx = random.randint(-2, 2) 
                dy = random.randint(-2, 2) 
                # print(f"DEBUG: generate_terrain cluster dx={dx}, dy={dy}") 
                neighbor_col, neighbor_row = cluster_center_col + dx, cluster_center_row + dy
                if 0 <= neighbor_col < grid_width and 0 <= neighbor_row < grid_height and random.random() > 0.4:
                    terrain_grid[neighbor_row][neighbor_col] = "stone"
    return terrain_grid

# -------------------------- Spatial Grid Class --------------------------
class SpatialGrid:
    def __init__(self, world_width, world_height, grid_cell_size):
        self.cell_size = grid_cell_size
        self.grid_width = math.ceil(world_width / grid_cell_size)
        self.grid_height = math.ceil(world_height / grid_cell_size)
        self.grid = [[[] for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def _get_grid_coords(self, world_x, world_y):
        return int(world_x // self.cell_size), int(world_y // self.cell_size)

    def add_object(self, obj, obj_rect):
        min_grid_col, min_grid_row = self._get_grid_coords(obj_rect.left, obj_rect.top)
        max_grid_col, max_grid_row = self._get_grid_coords(obj_rect.right, obj_rect.bottom)
        obj.grid_cells = set() 
        for grid_col in range(max(0, min_grid_col), min(self.grid_width, max_grid_col + 1)):
            for grid_row in range(max(0, min_grid_row), min(self.grid_height, max_grid_row + 1)):
                self.grid[grid_row][grid_col].append(obj)
                obj.grid_cells.add((grid_col, grid_row))
    
    def remove_object(self, obj):
        if hasattr(obj, 'grid_cells'):
            for grid_col, grid_row in obj.grid_cells:
                if 0 <= grid_col < self.grid_width and 0 <= grid_row < self.grid_height:
                    try:
                        self.grid[grid_row][grid_col].remove(obj)
                    except ValueError: 
                        pass
            if hasattr(obj, 'grid_cells'): 
                delattr(obj, 'grid_cells')


    def update_object_location(self, obj, new_rect):
        self.remove_object(obj)
        self.add_object(obj, new_rect)

    def query_radius(self, center_x, center_y, radius, exclude_obj=None):
        min_grid_col, min_grid_row = self._get_grid_coords(center_x - radius, center_y - radius)
        max_grid_col, max_grid_row = self._get_grid_coords(center_x + radius, center_y + radius)
        
        candidate_objects = set()
        for grid_col in range(max(0, min_grid_col), min(self.grid_width, max_grid_col + 1)):
            for grid_row in range(max(0, min_grid_row), min(self.grid_height, max_grid_row + 1)):
                for obj_item in self.grid[grid_row][grid_col]:
                    if obj_item is not exclude_obj:
                        candidate_objects.add(obj_item)
        
        nearby_objects = []
        for obj_item in candidate_objects:
            obj_item_rect = obj_item.get_bounding_rect() 
            dist_sq = (obj_item_rect.centerx - center_x)**2 + (obj_item_rect.centery - center_y)**2
            if dist_sq <= radius**2:
                nearby_objects.append(obj_item)
        return nearby_objects

    def query_rect(self, query_rect, exclude_obj=None):
        min_grid_col, min_grid_row = self._get_grid_coords(query_rect.left, query_rect.top)
        max_grid_col, max_grid_row = self._get_grid_coords(query_rect.right, query_rect.bottom)

        candidate_objects = set()
        for grid_col in range(max(0, min_grid_col), min(self.grid_width, max_grid_col + 1)):
            for grid_row in range(max(0, min_grid_row), min(self.grid_height, max_grid_row + 1)):
                for obj_item in self.grid[grid_row][grid_col]:
                     if obj_item is not exclude_obj:
                        candidate_objects.add(obj_item)
        
        colliding_objects = []
        for obj_item in candidate_objects:
            if query_rect.colliderect(obj_item.get_bounding_rect()): 
                colliding_objects.append(obj_item)
        return colliding_objects

    def get_objects_in_cell(self, grid_col, grid_row):
        if 0 <= grid_col < self.grid_width and 0 <= grid_row < self.grid_height:
            return self.grid[grid_row][grid_col]
        return []

# -------------------------- Meat Class --------------------------
class Meat:
    def __init__(self, x, y, energy, spawn_time, meat_type="red"):
        self.x, self.y, self.energy, self.spawn_time, self.meat_type = x, y, energy, spawn_time, meat_type
        self.width, self.height = CELL_SIZE, CELL_SIZE
        self._bounding_rect = pygame.Rect(self.x,self.y,self.width,self.height) 
    
    def get_bounding_rect(self): 
        return self._bounding_rect
    
    def draw(self, surface, camera):
        if not camera.is_rect_visible(self._bounding_rect): 
            return
        
        zoomed_size = camera.zoom*CELL_SIZE
        if zoomed_size < SETTINGS["meat_lod_min_pixel_size"] : 
            return

        screen_pos = camera.world_to_screen(self.x,self.y)
        color = GREEN_MEAT_COLOR if self.meat_type=="green" else RED_MEAT_COLOR
        pygame.draw.rect(surface,color,(screen_pos[0],screen_pos[1],math.ceil(zoomed_size),math.ceil(zoomed_size)))

# -------------------------- Species Class --------------------------
class Species:
    def __init__(self, world, x, y, parent=None):
        self.world, self.x, self.y = world, x, y
        self.id = generate_unique_id() 
        self.dead = False
        self.velocity_x, self.velocity_y = 0,0
        self.reproduction_timer = 0
        self.is_attacking, self.attack_target, self.action_intent = False, None, "idle"
        
        self._cached_surface = None
        self._is_dirty = True 
        self._cached_render_int_zoomed_cell_size = -1 
        
        self._bounding_rect = None 
        self._rect_dirty = True    

        self.target_search_cooldown_max = random.uniform(
            SETTINGS["target_search_cooldown_min_ms"], 
            SETTINGS["target_search_cooldown_max_ms"]
        )
        self.target_search_timer = self.target_search_cooldown_max 
        self.current_steering_target = None 

        self.sporadic_move_timer = 0
        self.sporadic_move_cooldown = random.uniform(
            SETTINGS["sporadic_move_cooldown_min_ms"],
            SETTINGS["sporadic_move_cooldown_max_ms"]
        )
        self.log_movement_event_timer = 0 
        self.log_movement_event_cooldown = random.uniform(3000, 7000) 

        if parent:
            self.energy = parent.energy * SETTINGS["child_energy_split_ratio"]
            parent.energy *= (1 - SETTINGS["child_energy_split_ratio"])
            self.grid_size = max(2, parent.grid_size + random.randint(-1,2)) 
            self._rect_dirty = True 
            self.cells = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            for row_index in range(min(self.grid_size, parent.grid_size)):
                for col_index in range(min(self.grid_size, parent.grid_size)):
                    self.cells[row_index][col_index] = parent.cells[row_index][col_index]
            self._mutate_cells(parent.mutation_rate) 
            self.max_energy = clamp(random_mutation(parent.max_energy, SETTINGS["max_energy_mutation_range"], parent.mutation_rate), 10, 10000)
            self.reproduction_cooldown = clamp(random_mutation(parent.reproduction_cooldown, SETTINGS["reproduction_cooldown_mutation_range"], parent.mutation_rate), SETTINGS["reproduction_cooldown"]*0.5, SETTINGS["reproduction_cooldown"]*2)
            self.mutation_rate = clamp(random_mutation(parent.mutation_rate, SETTINGS["mutation_rate_mutation_range"], parent.mutation_rate), 0.01, 0.5)
            self.brain_behavior = parent.brain_behavior if random.random() > self.mutation_rate else random.choice(["sporadic","hunter","passive_hunter"])
            self.lineage_id = parent.lineage_id 
            if random.random() < SETTINGS["lineage_id_mutation_chance"]: 
                self.lineage_id = generate_unique_id()
            self.reproduction_distance = clamp(random_mutation(parent.reproduction_distance, SETTINGS["reproduction_distance_mutation_range"], parent.mutation_rate), SETTINGS["min_reproduction_distance"], SETTINGS["max_reproduction_distance"])
        else: 
            self.energy = random.randint(SETTINGS["initial_energy_min"], SETTINGS["initial_energy_max"])
            self.grid_size = random.randint(3, 7) 
            self._rect_dirty = True 
            self.cells = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            self.brain_behavior = random.choice(["sporadic","hunter","passive_hunter","stationary"])
            self._populate_randomly() 
            self.max_energy = random.randint(SETTINGS["genetic_max_energy_min"], SETTINGS["genetic_max_energy_max"]) 
            self.reproduction_cooldown, self.mutation_rate = SETTINGS["reproduction_cooldown"], SETTINGS["mutation_rate_default"]
            self.lineage_id = generate_unique_id() 
            self.reproduction_distance = random.uniform(SETTINGS["initial_reproduction_distance_min"], SETTINGS["initial_reproduction_distance_max"])
        
        self.reproduction_threshold = self.max_energy * SETTINGS["reproduction_energy_ratio"]
        self._update_cached_properties() 
        self._is_dirty = True 

    def _populate_randomly(self):
        for row_index in range(self.grid_size):
            for col_index in range(self.grid_size):
                if random.random() > 0.3:
                    self.cells[row_index][col_index] = random.choice(list(CELL_COLORS.keys()))
        self._is_dirty = True
        self._rect_dirty = True 

    def _mutate_cells(self, mutation_rate):
        changed = False
        for row_index in range(self.grid_size):
            for col_index in range(self.grid_size):
                if random.random() < mutation_rate:
                    old_cell = self.cells[row_index][col_index]
                    if self.cells[row_index][col_index] is None or random.random() < 0.5:
                        self.cells[row_index][col_index] = random.choice(list(CELL_COLORS.keys()))
                    else:
                        self.cells[row_index][col_index] = None
                    if old_cell != self.cells[row_index][col_index]:
                        changed = True
        if changed:
            self._is_dirty = True
            self._rect_dirty = True 
            self._update_cached_properties() 

    def _update_cached_properties(self):
        self.has_roots, self.has_consumption, self.has_attack, self.has_eyes = False,False,False,False
        self.movement_cells_count, self.root_cells_count, self.num_attack_cells, self.vision_range = 0,0,0,0
        current_cost = SETTINGS["base_maintenance_cost"]
        for row_cells_list in self.cells:
            for cell_type in row_cells_list:
                if cell_type:
                    current_cost += SETTINGS["cell_maintenance_costs"].get(cell_type,0.1)
                    if cell_type=="roots": self.has_roots=True; self.root_cells_count+=1
                    elif cell_type=="consumption": self.has_consumption=True
                    elif cell_type=="attack": self.has_attack=True; self.num_attack_cells+=1
                    elif cell_type=="movement": self.movement_cells_count+=1
                    elif cell_type=="eyes": self.has_eyes=True; self.vision_range+=200
        self.maintenance_cost = current_cost
        self._is_dirty = True 
        self._rect_dirty = True

    def get_bounding_rect(self):
        if self._rect_dirty or self._bounding_rect is None:
            self._bounding_rect = pygame.Rect(self.x, self.y, 
                                              self.grid_size * CELL_SIZE, 
                                              self.grid_size * CELL_SIZE)
            self._rect_dirty = False
        return self._bounding_rect

    def get_center_pos(self): 
        return self.get_bounding_rect().centerx, self.get_bounding_rect().centery

    def _render_to_cache(self, camera_zoom_for_render):
        current_int_zoomed_cell_size = math.ceil(CELL_SIZE * camera_zoom_for_render)
        if current_int_zoomed_cell_size <= 0: 
            self._cached_surface = None
            self._cached_render_int_zoomed_cell_size = 0
            return

        surface_width = self.grid_size * current_int_zoomed_cell_size
        surface_height = self.grid_size * current_int_zoomed_cell_size

        if surface_width <= 0 or surface_height <= 0: 
            self._cached_surface = None
            self._cached_render_int_zoomed_cell_size = current_int_zoomed_cell_size
            return

        self._cached_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        # self._cached_surface.fill((0,0,0,0)) # SRCALPHA surfaces start transparent

        for row_idx, row_cells in enumerate(self.cells):
            for col_idx, cell_type in enumerate(row_cells):
                if cell_type:
                    cell_rect_on_cache = pygame.Rect(
                        col_idx * current_int_zoomed_cell_size,
                        row_idx * current_int_zoomed_cell_size,
                        current_int_zoomed_cell_size,
                        current_int_zoomed_cell_size
                    )
                    pygame.draw.rect(self._cached_surface, CELL_COLORS[cell_type], cell_rect_on_cache)
        
        self._is_dirty = False
        self._cached_render_int_zoomed_cell_size = current_int_zoomed_cell_size


    def steer_towards(self, target_x, target_y, max_allowed_speed=2.0):
        my_center_x, my_center_y = self.get_center_pos()
        delta_x, delta_y = target_x - my_center_x, target_y - my_center_y
        distance = math.hypot(delta_x, delta_y)
        if distance == 0: return
        delta_x /= distance; delta_y /= distance 
        steering_force_factor = 0.6 
        self.velocity_x += delta_x * steering_force_factor
        self.velocity_y += delta_y * steering_force_factor
        current_speed = math.hypot(self.velocity_x, self.velocity_y)
        if current_speed > max_allowed_speed:
            scale_factor = max_allowed_speed / current_speed
            self.velocity_x *= scale_factor; self.velocity_y *= scale_factor

    def move(self, dt_scaled):
        if self.has_roots or self.dead or self.movement_cells_count == 0:
            self.velocity_x *= 0.5; self.velocity_y *= 0.5 
            return
        speed_multiplier = min(self.movement_cells_count * 0.3, 3.0) 
        
        time_factor = dt_scaled / (1000.0 / 60.0) 

        delta_pos_x = self.velocity_x * speed_multiplier * time_factor
        delta_pos_y = self.velocity_y * speed_multiplier * time_factor


        if abs(delta_pos_x) > 0.01 or abs(delta_pos_y) > 0.01 : 
            self.x += delta_pos_x
            self.y += delta_pos_y
            self._rect_dirty = True 

        self.velocity_x *= 0.94 
        self.velocity_y *= 0.94 
        self.x %= self.world.width; self.y %= self.world.height 
        
        movement_effort = self.movement_cells_count * (math.hypot(self.velocity_x, self.velocity_y) + 0.1) 
        movement_energy_cost = movement_effort * SETTINGS["movement_cost_rate_per_velocity"] * (dt_scaled / 1000.0)
        self.energy -= movement_energy_cost
        
        if self._rect_dirty : 
            self.world.spatial_grid.update_object_location(self, self.get_bounding_rect())

    def consume_meat(self):
        if not self.has_consumption or self.has_roots or self.dead: return
        collection_rect = self.get_bounding_rect().inflate(CELL_SIZE, CELL_SIZE) 
        
        nearby_meat_items = self.world.spatial_grid.query_rect(collection_rect) 
        for meat_object in nearby_meat_items: 
            if not isinstance(meat_object, Meat): continue
            if meat_object not in self.world.meat_list: continue 

            if collection_rect.colliderect(meat_object.get_bounding_rect()):
                self.energy = min(self.max_energy, self.energy + meat_object.energy)
                self.world.log_event(type="consume_meat", location=self.get_center_pos(), primary_actor_id=self.id, value=meat_object.energy)
                self.world.remove_meat(meat_object) 
                if self.current_steering_target is meat_object:
                    self.current_steering_target = None 
                    self.target_search_timer = self.target_search_cooldown_max 
                # No break, consume all in range

    def reproduce(self):
        if self.reproduction_timer >= self.reproduction_cooldown and self.energy > self.reproduction_threshold:
            angle = random.uniform(0, 2 * math.pi)
            offset_x = math.cos(angle) * self.reproduction_distance
            offset_y = math.sin(angle) * self.reproduction_distance
            child_x, child_y = self.x + offset_x, self.y + offset_y
            child_x = clamp(child_x, 0, self.world.width - self.grid_size*CELL_SIZE) 
            child_y = clamp(child_y, 0, self.world.height - self.grid_size*CELL_SIZE)
            child_species = Species(self.world, child_x, child_y, parent=self)
            self.world.add_species(child_species)
            self.world.log_event(type="reproduce", location=self.get_center_pos(), primary_actor_id=self.id, secondary_actor_id=child_species.id)
            self.reproduction_timer = 0

    def attack(self, dt_scaled):
        self.action_intent = "attacking" if self.is_attacking and self.attack_target else self.action_intent
        if not self.has_attack or self.dead or self.num_attack_cells == 0 or self.has_roots:
            self.is_attacking, self.attack_target = False, None
            return
        
        current_attack_range = self.get_bounding_rect().width / 2 + SETTINGS["attack_range_bonus"] 
        my_center_x, my_center_y = self.get_center_pos()

        if self.is_attacking and self.attack_target:
            if self.attack_target.dead or self.attack_target.lineage_id == self.lineage_id:
                self.is_attacking, self.attack_target = False, None
                return
            target_center_x, target_center_y = self.attack_target.get_center_pos()
            delta_x, delta_y = target_center_x - my_center_x, target_center_y - my_center_y
            distance_sq = delta_x*delta_x + delta_y*delta_y
            if distance_sq > current_attack_range**2: 
                self.is_attacking, self.attack_target = False, None
            else: 
                energy_drain_this_frame = self.num_attack_cells * SETTINGS["energy_drain_per_attack_cell_per_second"] * (dt_scaled / 1000.0)
                actual_drain = min(energy_drain_this_frame, self.attack_target.energy)
                self.attack_target.energy -= actual_drain
                self.energy = min(self.max_energy, self.energy + actual_drain * SETTINGS["attack_energy_gain_ratio"])
                if SETTINGS["attack_maintenance_cost_per_second"] > 0:
                    attack_cost_this_frame = SETTINGS["attack_maintenance_cost_per_second"] * (dt_scaled / 1000.0)
                    self.energy -= attack_cost_this_frame
                if self.attack_target.energy <= 0:
                    self.attack_target.die() 
                    self.is_attacking, self.attack_target = False, None
                else: 
                    self.world.log_event(type="attack", location=(my_center_x, my_center_y), primary_actor_id=self.id, secondary_actor_id=self.attack_target.id) # Corrected location
                return 

        self.is_attacking, self.attack_target = False, None 
        query_radius = current_attack_range + self.vision_range * 0.1 
        potential_targets = self.world.spatial_grid.query_radius(my_center_x, my_center_y, query_radius, exclude_obj=self)
        closest_valid_target, min_dist_to_target_sq = None, float('inf')

        for other_species in potential_targets:
            if not isinstance(other_species, Species) or other_species.dead or other_species.lineage_id == self.lineage_id:
                continue
            other_center_x, other_center_y = other_species.get_center_pos()
            delta_x_other, delta_y_other = other_center_x - my_center_x, other_center_y - my_center_y
            current_dist_sq = delta_x_other*delta_x_other + delta_y_other*delta_y_other
            if current_dist_sq <= current_attack_range**2 and current_dist_sq < min_dist_to_target_sq:
                min_dist_to_target_sq, closest_valid_target = current_dist_sq, other_species
        
        if closest_valid_target:
            self.is_attacking, self.attack_target, self.action_intent = True, closest_valid_target, "attacking"
            self.world.log_event(type="attack", location=(my_center_x, my_center_y), primary_actor_id=self.id, secondary_actor_id=self.attack_target.id) # Corrected location


    def process_energy_from_roots(self, dt_scaled):
        # To-Do: Count The Amount Of Roots & Reduce Gain Per Root Exponentially For Every Extra Root -- DONE
        if not self.has_roots or self.dead: return
        self.action_intent = "rooting"
        terrain_grid_x, terrain_grid_y = int(self.get_center_pos()[0]//CELL_SIZE), int(self.get_center_pos()[1]//CELL_SIZE)
        gain_multiplier_from_terrain = 0 
        if 0 <= terrain_grid_y < len(self.world.terrain) and 0 <= terrain_grid_x < len(self.world.terrain[0]):
            tile_type = self.world.terrain[terrain_grid_y][terrain_grid_x]
            if tile_type=="dirt": gain_multiplier_from_terrain = 1
            elif tile_type=="saturated_dirt": gain_multiplier_from_terrain = 1.5
        
        if gain_multiplier_from_terrain > 0:
            base_absorption_rate = SETTINGS["plant_energy_absorption_rate_per_cell_per_second"]
            energy_gain_per_second = ((self.root_cells_count * gain_multiplier_from_terrain * base_absorption_rate) * (0.91 ** self.root_cells_count) * random.random() * 2)
            energy_gained_this_frame = energy_gain_per_second * (dt_scaled / 1000.0)
            self.energy = min(self.max_energy, self.energy + energy_gained_this_frame)
    
    def die(self):
        if self.dead: return
        self.dead, self.is_attacking, self.attack_target = True, False, None
        self.world.log_event(type="die", location=self.get_center_pos(), primary_actor_id=self.id)
        num_actual_cells = sum(1 for row in self.cells for cell_type in row if cell_type is not None)
        num_actual_cells = 1 if num_actual_cells == 0 else num_actual_cells 
        energy_per_meat = (self.energy / num_actual_cells) * 0.5 
        energy_per_meat = max(1, energy_per_meat) 
        for row_idx, row_cells_list in enumerate(self.cells):
            for col_idx, cell_type in enumerate(row_cells_list):
                if cell_type is not None:
                    meat_x, meat_y = self.x + col_idx*CELL_SIZE, self.y + row_idx*CELL_SIZE
                    self.world.add_meat(Meat(meat_x, meat_y, energy_per_meat, self.world.simulation_time, "red"))
    
    def _find_target_for_steering(self): 
        if not self.has_eyes or self.dead: self.action_intent = "idle"; return None
        target_for_steering, min_dist_sq = None, float('inf')
        my_center_x, my_center_y = self.get_center_pos()
        
        potential_entities = self.world.spatial_grid.query_radius(my_center_x, my_center_y, self.vision_range, exclude_obj=self)
        found_priority_target = False
        
        if self.brain_behavior == "hunter" or (self.brain_behavior == "passive_hunter" and self.energy < self.max_energy * 0.7):
            for entity in potential_entities:
                if isinstance(entity, Species) and not entity.dead and entity.lineage_id != self.lineage_id:
                    entity_center_x, entity_center_y = entity.get_center_pos()
                    dist_sq = (entity_center_x - my_center_x)**2 + (entity_center_y - my_center_y)**2
                    if dist_sq < min_dist_sq : 
                        min_dist_sq, target_for_steering, self.action_intent, found_priority_target = dist_sq, entity, "hunting", True
            if target_for_steering: return target_for_steering
        
        if self.has_consumption:
            min_dist_sq_meat, meat_target = float('inf'), None
            for entity in potential_entities: 
                if isinstance(entity, Meat) and entity in self.world.meat_list : 
                    entity_rect = entity.get_bounding_rect() 
                    entity_center_x, entity_center_y = entity_rect.centerx, entity_rect.centery
                    dist_sq = (entity_center_x - my_center_x)**2 + (entity_center_y - my_center_y)**2
                    if dist_sq < min_dist_sq_meat :
                        min_dist_sq_meat, meat_target = dist_sq, entity
            
            if meat_target:
                if not found_priority_target or (min_dist_sq_meat < min_dist_sq):
                    self.action_intent = "scavenging"; return meat_target
                elif found_priority_target and target_for_steering: 
                    self.action_intent = "hunting"; return target_for_steering
        
        if not target_for_steering: 
            self.action_intent = "wandering" if self.brain_behavior == "sporadic" else "idle"
        return target_for_steering

    def act(self, dt_scaled, is_allowed_full_ai_search): 
        if self.dead: return
        
        if self.brain_behavior == "stationary": self.action_intent = "stationary"
        elif self.has_roots: self.action_intent = "rooting"
        else: self.action_intent = "idle" 

        self.energy -= self.maintenance_cost * (dt_scaled / 1000.0)
        if self.energy <= 0: self.die(); return
        
        self.reproduction_timer += dt_scaled
        self.attack(dt_scaled) 
        
        self.target_search_timer += dt_scaled
        if self.brain_behavior != "stationary" and not self.is_attacking:
            target_invalidated_this_frame = False
            if self.current_steering_target:
                if (isinstance(self.current_steering_target, Species) and self.current_steering_target.dead) or \
                   (isinstance(self.current_steering_target, Meat) and self.current_steering_target not in self.world.meat_list): 
                    self.current_steering_target = None
                    target_invalidated_this_frame = True
            
            time_for_proactive_search = self.target_search_timer >= self.target_search_cooldown_max
            
            needs_new_target_search = False
            if self.current_steering_target is None: 
                if target_invalidated_this_frame: 
                    needs_new_target_search = True
                elif is_allowed_full_ai_search: 
                     needs_new_target_search = True
            elif time_for_proactive_search and is_allowed_full_ai_search: 
                needs_new_target_search = True


            if needs_new_target_search:
                if self.has_eyes:
                    self.current_steering_target = self._find_target_for_steering() 
                self.target_search_timer = 0 
            
            if self.current_steering_target:
                target_pos = self.current_steering_target.get_center_pos() if isinstance(self.current_steering_target, Species) else self.current_steering_target.get_bounding_rect().center
                self.steer_towards(target_pos[0], target_pos[1])
                if not self.is_attacking: 
                    if isinstance(self.current_steering_target, Species): self.action_intent = "hunting"
                    elif isinstance(self.current_steering_target, Meat): self.action_intent = "scavenging"
            elif self.brain_behavior == "sporadic": 
                self.sporadic_move_timer += dt_scaled
                if self.sporadic_move_timer >= self.sporadic_move_cooldown:
                    self.velocity_x += random.uniform(-1, 1) 
                    self.velocity_y += random.uniform(-1, 1)
                    self.sporadic_move_timer = 0
                    self.sporadic_move_cooldown = random.uniform(
                        SETTINGS["sporadic_move_cooldown_min_ms"],
                        SETTINGS["sporadic_move_cooldown_max_ms"]
                    )
                if self.action_intent == "idle": self.action_intent = "wandering" 
        
        # Log active movement for cinematic mode
        self.log_movement_event_timer += dt_scaled
        if self.action_intent in ["hunting", "scavenging"] and self.log_movement_event_timer >= self.log_movement_event_cooldown:
            if math.hypot(self.velocity_x, self.velocity_y) > 0.1: # Only log if actually moving
                self.world.log_event(type="active_movement", location=self.get_center_pos(), primary_actor_id=self.id)
                self.log_movement_event_timer = 0
                self.log_movement_event_cooldown = random.uniform(3000, 7000) # Reset cooldown

        if self.has_roots: self.process_energy_from_roots(dt_scaled) 
        
        self.move(dt_scaled)
        if not self.is_attacking: self.consume_meat() 
        self.reproduce()

        if not self.is_attacking and not self.has_roots and \
           self.brain_behavior != "stationary" and self.current_steering_target is None and \
           self.action_intent not in ["hunting", "scavenging", "wandering", "rooting", "attacking", "stationary"]:
            self.action_intent = "idle"
    
    def draw(self, surface, camera):
        if self.dead: return
        
        if not camera.is_rect_visible(self.get_bounding_rect()): return

        current_int_zoomed_cell_size = math.ceil(CELL_SIZE * camera.zoom)
        if self._is_dirty or self._cached_surface is None or self._cached_render_int_zoomed_cell_size != current_int_zoomed_cell_size:
            if current_int_zoomed_cell_size > 0 : 
                 self._render_to_cache(camera.zoom)
            else: 
                self._cached_surface = None 
                self._cached_render_int_zoomed_cell_size = current_int_zoomed_cell_size 
        
        if self._cached_surface:
            screen_pos_top_left = camera.world_to_screen(self.x, self.y)
            surface.blit(self._cached_surface, screen_pos_top_left)
        
        if camera.zoom >= SETTINGS["species_ui_zoom_threshold"]:
            indicator_world_x, indicator_world_y = self.get_center_pos()[0], self.y - 10 
            indicator_screen_pos = camera.world_to_screen(indicator_world_x, indicator_world_y)
            if self.has_roots: 
                base_rect_height = CELL_SIZE * self.grid_size * 0.25 * camera.zoom 
                base_rect_width = CELL_SIZE * self.grid_size * 0.8 * camera.zoom 
                base_screen_x, base_screen_y = camera.world_to_screen(self.x + CELL_SIZE*self.grid_size*0.1, self.y + CELL_SIZE*self.grid_size*0.75) 
                pygame.draw.rect(surface, PLANT_INDICATOR_COLOR, (base_screen_x, base_screen_y, base_rect_width, base_rect_height), border_radius=max(1,int(2*camera.zoom)))
            else: 
                indicator_color = INTENT_COLORS.get(self.action_intent, INTENT_COLORS["idle"])
                pygame.draw.circle(surface, indicator_color, (int(indicator_screen_pos[0]), int(indicator_screen_pos[1])), int(INTENT_INDICATOR_RADIUS * max(1, camera.zoom*0.5)))

            if self.is_attacking and self.attack_target:
                my_center_screen = camera.world_to_screen(*self.get_center_pos())
                target_center_screen = camera.world_to_screen(*self.attack_target.get_center_pos())
                min_x, max_x = min(my_center_screen[0],target_center_screen[0]), max(my_center_screen[0],target_center_screen[0])
                min_y, max_y = min(my_center_screen[1],target_center_screen[1]), max(my_center_screen[1],target_center_screen[1])
                line_surface_width, line_surface_height = max_x - min_x + 4, max_y - min_y + 4
                if line_surface_width > 0 and line_surface_height > 0:
                    line_surface = pygame.Surface((line_surface_width, line_surface_height), pygame.SRCALPHA)
                    start_on_surface = (my_center_screen[0]-min_x+2, my_center_screen[1]-min_y+2)
                    end_on_surface = (target_center_screen[0]-min_x+2, target_center_screen[1]-min_y+2)
                    pygame.draw.line(line_surface, ATTACK_LINE_COLOR, start_on_surface, end_on_surface, max(1,int(2*camera.zoom*0.75)))
                    surface.blit(line_surface, (min_x-2, min_y-2))
            
            bar_width, bar_height = 30*camera.zoom, 5*camera.zoom
            bar_screen_pos = camera.world_to_screen(self.x + (self.grid_size*CELL_SIZE/2) - (bar_width/(2*camera.zoom)), self.y-5)
            energy_ratio = clamp(self.energy/self.max_energy,0,1)
            current_energy_width = bar_width * energy_ratio
            bar_color = ENERGY_LOW_COLOR
            if energy_ratio > 0.66: bar_color = ENERGY_HIGH_COLOR
            elif energy_ratio > 0.33: bar_color = ENERGY_MID_COLOR
            pygame.draw.rect(surface, ENERGY_BAR_BACKGROUND, (bar_screen_pos[0],bar_screen_pos[1],bar_width,bar_height))
            pygame.draw.rect(surface, bar_color, (bar_screen_pos[0],bar_screen_pos[1],current_energy_width,bar_height))

# -------------------------- World Class --------------------------
class World:
    def __init__(self, width, height, initial_population_size):
        self.width, self.height, self.initial_population_size = width, height, initial_population_size
        self.terrain = generate_terrain(width, height, CELL_SIZE)
        self.spatial_grid = SpatialGrid(width, height, SETTINGS["spatial_grid_cell_size"])
        self.species_list, self.meat_list = [], []
        self.simulation_time, self.last_green_meat_spawn = 0,0
        
        self.chunk_tile_size = SETTINGS["terrain_chunk_size"] 
        self.chunk_pixel_size = self.chunk_tile_size * CELL_SIZE 
        self.terrain_chunk_cache = {}
        self.terrain_chunk_render_int_tile_size = {} 
        self.dirty_chunks = set() 
        self._initialize_terrain_chunks()

        self.current_ai_update_index = 0
        self.species_allowed_full_search_this_frame = set()
        self.event_log = [] 


        min_sep = SETTINGS["min_initial_spawn_separation"]
        for _ in range(initial_population_size):
            placed_successfully = False
            spawn_x = random.randint(0,width-5*CELL_SIZE) # Corrected
            spawn_y = random.randint(0,height-5*CELL_SIZE) # Corrected
            # print(f"DEBUG: Attempting spawn at ({spawn_x}, {spawn_y})") 
            for _ in range(10): 
                too_close = False
                for existing_species in self.species_list:
                    dist_sq = (spawn_x - existing_species.x)**2 + (spawn_y - existing_species.y)**2
                    if dist_sq < min_sep**2:
                        too_close = True; break
                if not too_close:
                    self.add_species(Species(self,spawn_x,spawn_y)); placed_successfully = True; break
                spawn_x = random.randint(0,width-5*CELL_SIZE) # Corrected
                spawn_y = random.randint(0,height-5*CELL_SIZE) # Corrected
                # print(f"DEBUG: Retrying spawn at ({spawn_x}, {spawn_y})") 
            if not placed_successfully: 
                self.add_species(Species(self,spawn_x,spawn_y)) 

    def log_event(self, type, location, primary_actor_id=None, secondary_actor_id=None, value=None):
        """Logs an interesting event for potential cinematic tracking."""
        score = SETTINGS["cinematic_event_interest_scores"].get(type, 1) 
        self.event_log.append({
            "id": generate_unique_id(), 
            "type": type,
            "location": location, 
            "primary_actor_id": primary_actor_id,
            "secondary_actor_id": secondary_actor_id,
            "value": value, 
            "timestamp": self.simulation_time,
            "interest_score": score,
            "viewed_fully": False 
        })
        if len(self.event_log) > 100: 
            self.event_log.pop(0)


    def _initialize_terrain_chunks(self):
        num_chunks_x = math.ceil(self.width / self.chunk_pixel_size)
        num_chunks_y = math.ceil(self.height / self.chunk_pixel_size)
        for cx in range(num_chunks_x):
            for cy in range(num_chunks_y):
                self.dirty_chunks.add((cx,cy)) 

    def _render_terrain_chunk(self, chunk_col, chunk_row, camera_zoom_for_render):
        int_zoomed_tile_size = math.ceil(CELL_SIZE * camera_zoom_for_render)
        if int_zoomed_tile_size <= 0: 
             self.terrain_chunk_cache[(chunk_col, chunk_row)] = None 
             self.terrain_chunk_render_int_tile_size[(chunk_col,chunk_row)] = 0 
             return

        chunk_surface_pixel_width = self.chunk_tile_size * int_zoomed_tile_size
        chunk_surface_pixel_height = self.chunk_tile_size * int_zoomed_tile_size
        
        if chunk_surface_pixel_width <= 0 or chunk_surface_pixel_height <= 0:
            self.terrain_chunk_cache[(chunk_col, chunk_row)] = None
            self.terrain_chunk_render_int_tile_size[(chunk_col,chunk_row)] = int_zoomed_tile_size 
            return

        chunk_surface = pygame.Surface((chunk_surface_pixel_width, chunk_surface_pixel_height))
        
        start_tile_col = chunk_col * self.chunk_tile_size
        start_tile_row = chunk_row * self.chunk_tile_size
        
        for r_offset in range(self.chunk_tile_size):
            for c_offset in range(self.chunk_tile_size):
                tile_world_row = start_tile_row + r_offset
                tile_world_col = start_tile_col + c_offset

                if tile_world_row < len(self.terrain) and tile_world_col < len(self.terrain[0]):
                    tile_type = self.terrain[tile_world_row][tile_world_col]
                    tile_color = BROWN 
                    if tile_type=="dirt": tile_color = BROWN
                    elif tile_type=="saturated_dirt": tile_color = SATURATED_DIRT_BROWN
                    elif tile_type=="stone": tile_color = STONE_GRAY
                    
                    tile_x_on_chunk = c_offset * int_zoomed_tile_size
                    tile_y_on_chunk = r_offset * int_zoomed_tile_size
                    pygame.draw.rect(chunk_surface, tile_color, 
                                     (tile_x_on_chunk, tile_y_on_chunk, int_zoomed_tile_size, int_zoomed_tile_size))
        
        self.terrain_chunk_cache[(chunk_col, chunk_row)] = chunk_surface
        self.terrain_chunk_render_int_tile_size[(chunk_col, chunk_row)] = int_zoomed_tile_size 
        if (chunk_col, chunk_row) in self.dirty_chunks:
            self.dirty_chunks.remove((chunk_col, chunk_row))


    def add_species(self, species_obj):
        self.species_list.append(species_obj)
        self.spatial_grid.add_object(species_obj, species_obj.get_bounding_rect())
    def remove_species(self, species_obj):
        if species_obj in self.species_list:
            self.species_list.remove(species_obj)
            self.spatial_grid.remove_object(species_obj)
    def add_meat(self, meat_item):
        if len(self.meat_list) >= SETTINGS["max_total_meat_items"]:
            if self.meat_list: 
                oldest_meat = self.meat_list.pop(0) 
                self.spatial_grid.remove_object(oldest_meat)
        
        self.meat_list.append(meat_item)
        self.spatial_grid.add_object(meat_item, meat_item.get_bounding_rect())

    def remove_meat(self, meat_item):
        if meat_item in self.meat_list: 
            self.meat_list.remove(meat_item)
            self.spatial_grid.remove_object(meat_item) 

    def _spawn_natural_green_meat(self):
        cluster_center_x, cluster_center_y = random.randint(0,self.width-CELL_SIZE), random.randint(0,self.height-CELL_SIZE)
        num_pieces = random.randint(SETTINGS["green_meat_cluster_min_size"], SETTINGS["green_meat_cluster_max_size"])
        for _ in range(num_pieces):
            offset_x = random.randint(-SETTINGS["green_meat_cluster_radius"], SETTINGS["green_meat_cluster_radius"])
            offset_y = random.randint(-SETTINGS["green_meat_cluster_radius"], SETTINGS["green_meat_cluster_radius"])
            # print(f"DEBUG: Spawning green meat with offset_x={offset_x}, offset_y={offset_y}") 
            meat_x = clamp(cluster_center_x+offset_x, 0, self.width-CELL_SIZE)
            meat_y = clamp(cluster_center_y+offset_y, 0, self.height-CELL_SIZE)
            self.add_meat(Meat(meat_x,meat_y,SETTINGS["green_meat_energy_value"],self.simulation_time,"green"))

    def _update_meat_decay(self):
        current_time = self.simulation_time
        for i in range(len(self.meat_list) - 1, -1, -1):
            meat_item = self.meat_list[i]
            if current_time - meat_item.spawn_time > SETTINGS["meat_decay_time"]:
                terrain_col, terrain_row = int(meat_item.x//CELL_SIZE), int(meat_item.y//CELL_SIZE)
                if 0 <= terrain_row < len(self.terrain) and 0 <= terrain_col < len(self.terrain[0]):
                    if self.terrain[terrain_row][terrain_col]=="dirt":
                        self.terrain[terrain_row][terrain_col]="saturated_dirt"
                        chunk_col = terrain_col // self.chunk_tile_size
                        chunk_row = terrain_row // self.chunk_tile_size
                        self.dirty_chunks.add((chunk_col, chunk_row))
                self.remove_meat(meat_item) 


    def _process_overcrowding(self):
        for grid_row_idx in range(self.spatial_grid.grid_height):
            for grid_col_idx in range(self.spatial_grid.grid_width):
                species_in_cell = [obj for obj in self.spatial_grid.get_objects_in_cell(grid_col_idx,grid_row_idx) if isinstance(obj,Species) and not obj.dead]
                if len(species_in_cell) > SETTINGS["overcrowding_limit"]:
                    num_to_kill = len(species_in_cell) - SETTINGS["overcrowding_limit"]
                    random.shuffle(species_in_cell)
                    for i in range(num_to_kill):
                        if species_in_cell[i] and not species_in_cell[i].dead:
                            species_in_cell[i].die()

    def update(self, dt_scaled):
        self.simulation_time += dt_scaled
        if self.simulation_time - self.last_green_meat_spawn > SETTINGS["green_meat_spawn_interval"]:
            self._spawn_natural_green_meat()
            self.last_green_meat_spawn = self.simulation_time
        self._update_meat_decay()

        self.species_allowed_full_search_this_frame.clear()
        if self.species_list: 
            stagger = max(1, SETTINGS["ai_update_stagger_factor"]) 
            num_species_to_update = math.ceil(len(self.species_list) / stagger)
            num_species_to_update = max(1, num_species_to_update) 
            
            for i in range(num_species_to_update):
                idx_to_update = (self.current_ai_update_index + i) % len(self.species_list)
                self.species_allowed_full_search_this_frame.add(self.species_list[idx_to_update])
            self.current_ai_update_index = (self.current_ai_update_index + num_species_to_update) % len(self.species_list)
        
        for species_obj in self.species_list:
            is_allowed_full_search = species_obj in self.species_allowed_full_search_this_frame
            species_obj.act(dt_scaled, is_allowed_full_search) 

        self._process_overcrowding()
        dead_species_found = [s for s in self.species_list if s.dead] 
        for dead_s in dead_species_found:
            self.remove_species(dead_s)

    def draw_terrain(self, surface, camera): 
        view_rect_world = camera.get_view_rect_world()
        
        start_chunk_col = max(0, int(view_rect_world.left // self.chunk_pixel_size))
        end_chunk_col = min(math.ceil(self.width / self.chunk_pixel_size), 
                            math.ceil(view_rect_world.right / self.chunk_pixel_size))
        start_chunk_row = max(0, int(view_rect_world.top // self.chunk_pixel_size))
        end_chunk_row = min(math.ceil(self.height / self.chunk_pixel_size),
                            math.ceil(view_rect_world.bottom / self.chunk_pixel_size))

        current_chunk_render_tile_size = math.ceil(CELL_SIZE * camera.zoom)

        for c_col in range(start_chunk_col, end_chunk_col):
            for c_row in range(start_chunk_row, end_chunk_row):
                chunk_key = (c_col, c_row)
                
                cached_chunk_int_tile_size = self.terrain_chunk_render_int_tile_size.get(chunk_key, -1)

                if chunk_key in self.dirty_chunks or \
                   cached_chunk_int_tile_size != current_chunk_render_tile_size or \
                   chunk_key not in self.terrain_chunk_cache:
                    self._render_terrain_chunk(c_col, c_row, camera.zoom) 
                
                cached_chunk_surface = self.terrain_chunk_cache.get(chunk_key)
                if cached_chunk_surface:
                    chunk_world_x = c_col * self.chunk_pixel_size
                    chunk_world_y = c_row * self.chunk_pixel_size
                    screen_pos = camera.world_to_screen(chunk_world_x, chunk_world_y)
                    surface.blit(cached_chunk_surface, screen_pos) 


    def draw_entities(self, surface, camera): 
        for meat_item in self.meat_list: meat_item.draw(surface,camera)
        for species_obj in self.species_list: species_obj.draw(surface,camera) 

# -------------------------- Camera Class --------------------------
class Camera:
    def __init__(self,x,y,screen_width,screen_height,world_width,world_height):
        self.x,self.y,self.zoom = x,y,SETTINGS["zoom_initial"]
        self.screen_width,self.screen_height,self.world_width,self.world_height = screen_width,screen_height,world_width,world_height
        self.target_x, self.target_y = x, y 
        self.target_zoom = SETTINGS["zoom_initial"] 
        self._clamp_to_world_bounds()

    def world_to_screen(self,world_x,world_y):
        return (world_x-self.x)*self.zoom+self.screen_width/2, (world_y-self.y)*self.zoom+self.screen_height/2
    def screen_to_world(self,screen_x,screen_y):
        return (screen_x-self.screen_width/2)/self.zoom+self.x, (screen_y-self.screen_height/2)/self.zoom+self.y
    
    def move(self,delta_x_world,delta_y_world):
        self.target_x += delta_x_world 
        self.target_y += delta_y_world
        self.x += delta_x_world; self.y += delta_y_world; self._clamp_to_world_bounds()

    def set_zoom(self,new_zoom,mouse_world_pos_before_zoom):
        old_zoom=self.zoom; self.zoom=clamp(new_zoom,SETTINGS["zoom_min"],SETTINGS["zoom_max"])
        self.target_zoom = self.zoom 
        if abs(old_zoom - self.zoom) > 0.0001: 
            self.x = mouse_world_pos_before_zoom[0] - ((mouse_world_pos_before_zoom[0]-self.x)*old_zoom)/self.zoom
            self.y = mouse_world_pos_before_zoom[1] - ((mouse_world_pos_before_zoom[1]-self.y)*old_zoom)/self.zoom
            self._clamp_to_world_bounds()
            self.target_x, self.target_y = self.x, self.y 

    def _clamp_to_world_bounds(self):
        visible_world_w = self.screen_width / max(self.zoom, 0.001) 
        visible_world_h = self.screen_height / max(self.zoom, 0.001)
        if self.world_width <= visible_world_w : self.x = self.world_width / 2
        else: self.x = clamp(self.x, visible_world_w / 2, self.world_width - visible_world_w / 2)
        if self.world_height <= visible_world_h: self.y = self.world_height / 2
        else: self.y = clamp(self.y, visible_world_h / 2, self.world_height - visible_world_h / 2)
        
        if self.world_width <= visible_world_w : self.target_x = self.world_width / 2
        else: self.target_x = clamp(self.target_x, visible_world_w / 2, self.world_width - visible_world_w / 2)
        if self.world_height <= visible_world_h: self.target_y = self.world_height / 2
        else: self.target_y = clamp(self.target_y, visible_world_h / 2, self.world_height - visible_world_h / 2)


    def get_view_rect_world(self):
        visible_world_w,visible_world_h = self.screen_width/max(self.zoom,0.001), self.screen_height/max(self.zoom,0.001)
        return pygame.Rect(self.x-visible_world_w/2, self.y-visible_world_h/2, visible_world_w, visible_world_h)
    def is_rect_visible(self,world_rect):
        return self.get_view_rect_world().colliderect(world_rect)

    def update_cinematic(self, dt_scaled):
        lerp_speed = SETTINGS["cinematic_camera_lerp_speed"]
        self.x += (self.target_x - self.x) * lerp_speed 
        self.y += (self.target_y - self.y) * lerp_speed
        self.zoom += (self.target_zoom - self.zoom) * lerp_speed
        self._clamp_to_world_bounds()


# -------------------------- Game Class --------------------------
class Game:
    def __init__(self):
        pygame.init();pygame.font.init()
        self.screen=pygame.display.set_mode((SETTINGS["screen_width"],SETTINGS["screen_height"]))
        pygame.display.set_caption('EVOSIM 2D');self.clock=pygame.time.Clock()
        self.font,self.small_font=pygame.font.SysFont("Arial",18),pygame.font.SysFont("Arial",14)
        
        self.game_state = STATE_MAIN_MENU 
        self.world = None 
        self.camera = None 

        self.time_rate = SETTINGS["default_time_rate"] 
        self.running=True
        self.dragging_camera,self.dragging_slider,self.last_drag_mouse_pos=False,False,None
        self.active_touches,self.last_pinch_distance={},None
        
        self.settings_menu_active = False 
        self.menu_item_rects = {} 
        self.main_menu_buttons = {}
        self.settings_menu_page = "Display" 
        self.settings_page_buttons = {}
        self.settings_step_multiplier = 1.0 
        self.multiplier_button_rects = {}


        self.cinematic_mode_active = SETTINGS["cinematic_mode_default_on"] 
        self.cinematic_current_focus_event_id = None 
        self.cinematic_focus_duration_timer = 0 
        self.cinematic_pan_target_pos = None
        self.cinematic_pan_timer_ms = 0


        self.menu_button_text_surface = self.small_font.render("[M] Menu", True, BLACK)
        self.menu_button_rect = pygame.Rect(SETTINGS["screen_width"] - self.menu_button_text_surface.get_width() - 30, 10, 
                                           self.menu_button_text_surface.get_width() + 20, self.menu_button_text_surface.get_height() + 10)

    def initialize_simulation(self):
        """Initializes or re-initializes the simulation world and camera."""
        self.world=World(SETTINGS["world_width"],SETTINGS["world_height"],SETTINGS["population_size"])
        self.camera=Camera(SETTINGS["world_width"]/2,SETTINGS["world_height"]/2,
                           SETTINGS["screen_width"],SETTINGS["screen_height"],
                           SETTINGS["world_width"],SETTINGS["world_height"])
        self.time_rate = SETTINGS["default_time_rate"] 
        self.cinematic_mode_active = SETTINGS["cinematic_mode_default_on"] 
        self.cinematic_current_focus_event_id = None
        self.cinematic_focus_duration_timer = 0
        self.cinematic_pan_target_pos = None
        self.cinematic_pan_timer_ms = 0


    def _handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.game_state == STATE_MAIN_MENU:
            self._handle_input_main_menu(mouse_pos)
        elif self.game_state == STATE_PRE_GAME_SETTINGS:
            self._handle_input_settings_menu(mouse_pos, is_pre_game=True)
        elif self.game_state == STATE_SIMULATION:
            self._handle_input_simulation(mouse_pos)
        elif self.game_state == STATE_IN_GAME_SETTINGS_MENU:
            self._handle_input_settings_menu(mouse_pos, is_pre_game=False)


    def _handle_input_main_menu(self, mouse_pos):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:self.running=False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, rect in self.main_menu_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if action == "start":
                            self.initialize_simulation()
                            self.game_state = STATE_SIMULATION
                        elif action == "settings":
                            self.settings_menu_page = "Display" 
                            self.game_state = STATE_PRE_GAME_SETTINGS
                        elif action == "quit":
                            self.running = False
                        return 

    def _handle_input_settings_menu(self, mouse_pos, is_pre_game):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:self.running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_m: 
                    self.game_state = STATE_MAIN_MENU if is_pre_game else STATE_SIMULATION
                    self.menu_item_rects.clear()
                    self.settings_page_buttons.clear()
                    self.multiplier_button_rects.clear()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check multiplier buttons first
                for mult_text, (rect, mult_val) in self.multiplier_button_rects.items():
                    if rect.collidepoint(mouse_pos):
                        self.settings_step_multiplier = mult_val
                        return # Multiplier click handled, redraw menu

                for page_name, rect in self.settings_page_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        self.settings_menu_page = page_name
                        self.menu_item_rects.clear() 
                        return
                self._handle_menu_item_click(mouse_pos) 

    def _handle_input_simulation(self, mouse_pos):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:self.running=False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_button_rect.collidepoint(mouse_pos):
                    self.settings_menu_active = True 
                    self.game_state = STATE_IN_GAME_SETTINGS_MENU
                    self.settings_menu_page = "Display" 
                    self.menu_item_rects.clear() 
                    self.multiplier_button_rects.clear()
                    continue 

            if event.type==pygame.FINGERDOWN:
                self.active_touches[event.finger_id]=(event.x*SETTINGS["screen_width"],event.y*SETTINGS["screen_height"])
                if len(self.active_touches)!=2:self.last_pinch_distance=None
            elif event.type==pygame.FINGERMOTION:
                if event.finger_id in self.active_touches:
                    self.active_touches[event.finger_id]=(event.x*SETTINGS["screen_width"],event.y*SETTINGS["screen_height"])
                    if len(self.active_touches)==2:
                        p1,p2=list(self.active_touches.values())
                        current_distance=math.hypot(p1[0]-p2[0],p1[1]-p2[1])
                        if self.last_pinch_distance is not None:
                            delta_distance=current_distance-self.last_pinch_distance
                            zoom_change=delta_distance*SETTINGS["pinch_zoom_sensitivity"]
                            mid_screen_x,mid_screen_y=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2
                            world_mid_before_zoom=self.camera.screen_to_world(mid_screen_x,mid_screen_y)
                            self.camera.set_zoom(self.camera.zoom+zoom_change,world_mid_before_zoom)
                        self.last_pinch_distance=current_distance
            elif event.type==pygame.FINGERUP:
                if event.finger_id in self.active_touches:del self.active_touches[event.finger_id]
                if len(self.active_touches)!=2:self.last_pinch_distance=None
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1: 
                    if SETTINGS["time_slider_rect"].collidepoint(mouse_pos):
                        self.dragging_slider=True;self._update_time_slider(mouse_pos[0])
                    elif not self.menu_button_rect.collidepoint(mouse_pos): 
                        self.dragging_camera=True;self.last_drag_mouse_pos=mouse_pos
                        self.cinematic_mode_active = False 
                elif event.button==4: 
                    mouse_world_pos_before_zoom=self.camera.screen_to_world(*mouse_pos)
                    self.camera.set_zoom(self.camera.zoom+SETTINGS["zoom_step"],mouse_world_pos_before_zoom)
                    self.cinematic_mode_active = False
                elif event.button==5: 
                    mouse_world_pos_before_zoom=self.camera.screen_to_world(*mouse_pos)
                    self.camera.set_zoom(self.camera.zoom-SETTINGS["zoom_step"],mouse_world_pos_before_zoom)
                    self.cinematic_mode_active = False
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:self.dragging_camera,self.dragging_slider,self.last_drag_mouse_pos=False,False,None
            elif event.type==pygame.MOUSEMOTION:
                if self.dragging_camera and self.last_drag_mouse_pos:
                    delta_screen_x,delta_screen_y = mouse_pos[0]-self.last_drag_mouse_pos[0],mouse_pos[1]-self.last_drag_mouse_pos[1]
                    self.camera.move(-delta_screen_x/self.camera.zoom,-delta_screen_y/self.camera.zoom)
                    self.last_drag_mouse_pos=mouse_pos
                    self.cinematic_mode_active = False
                elif self.dragging_slider:self._update_time_slider(mouse_pos[0])
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_m:
                    self.settings_menu_active=True 
                    self.game_state = STATE_IN_GAME_SETTINGS_MENU
                    self.settings_menu_page = "Display"
                    self.menu_item_rects.clear()
                    self.multiplier_button_rects.clear()
                elif event.key == pygame.K_c:
                    self.cinematic_mode_active = not self.cinematic_mode_active
                    if not self.cinematic_mode_active: 
                        self.camera.target_x, self.camera.target_y = self.camera.x, self.camera.y
                        self.camera.target_zoom = self.camera.zoom


    def _update_time_slider(self,mouse_x_pos):
        slider_rect=SETTINGS["time_slider_rect"]
        relative_x=clamp(mouse_x_pos-slider_rect.x,0,slider_rect.width)
        time_range = SETTINGS["time_slider_max"]-SETTINGS["time_slider_min"]
        self.time_rate = SETTINGS["time_slider_min"] + (relative_x/slider_rect.width)*time_range if time_range != 0 else SETTINGS["time_slider_min"]
        self.time_rate=clamp(self.time_rate,SETTINGS["time_slider_min"],SETTINGS["time_slider_max"])
        SETTINGS["default_time_rate"]=self.time_rate 
    
    def _draw_button(self, surface, text, rect, base_color, hover_color, text_color, font_to_use):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = hover_color if is_hovered else base_color
        pygame.draw.rect(surface, color, rect, border_radius=8)
        pygame.draw.rect(surface, MENU_BUTTON_BORDER_COLOR, rect, 2, border_radius=8)
        text_surf = font_to_use.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
        return is_hovered

    def _draw_main_menu(self):
        self.screen.fill(LIGHT_GRAY)
        title_font = pygame.font.SysFont("Arial", 72)
        title_surf = title_font.render("EVOSIM 2D", True, DARK_GRAY)
        title_rect = title_surf.get_rect(center=(SETTINGS["screen_width"]/2, SETTINGS["screen_height"]/4))
        self.screen.blit(title_surf, title_rect)

        button_width, button_height = 200, 50
        start_y = SETTINGS["screen_height"]/2 - 30
        
        self.main_menu_buttons["start"] = pygame.Rect(SETTINGS["screen_width"]/2 - button_width/2, start_y, button_width, button_height)
        self.main_menu_buttons["settings"] = pygame.Rect(SETTINGS["screen_width"]/2 - button_width/2, start_y + 70, button_width, button_height)
        self.main_menu_buttons["quit"] = pygame.Rect(SETTINGS["screen_width"]/2 - button_width/2, start_y + 140, button_width, button_height)

        self._draw_button(self.screen, "Start Simulation", self.main_menu_buttons["start"], MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.font)
        self._draw_button(self.screen, "Settings", self.main_menu_buttons["settings"], MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.font)
        self._draw_button(self.screen, "Quit", self.main_menu_buttons["quit"], MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.font)
        # pygame.display.flip() # Flip is in main loop

    def _draw_menu_item(self,surface,text_label,current_value,y_position,item_key_name,is_integer=False,step_val_override=None, min_val=None, max_val=None, is_dict_val=False, dict_key=None):
        val_to_display = current_value
        if is_dict_val and dict_key is not None:
            val_to_display = current_value.get(dict_key, "N/A")

        display_value_str = ""
        if item_key_name == "cinematic_mode_default_on": 
            display_value_str = "ON" if val_to_display else "OFF"
        elif isinstance(val_to_display, tuple): 
            display_value_str = str(val_to_display)
        elif is_integer: 
            display_value_str = f"{int(val_to_display)}"
        else: 
            display_value_str = f"{val_to_display:.2f}"
        
        if not isinstance(val_to_display, tuple) and item_key_name != "cinematic_mode_default_on":
            if item_key_name == "atk_range": display_value_str = f"{val_to_display/CELL_SIZE:.1f}x CELL_SIZE" 
            if item_key_name == "movement_cost_rate_per_velocity": display_value_str = f"{val_to_display:.4f}" 
            if item_key_name == "mutation_rate_default": display_value_str = f"{val_to_display:.3f}" 
            if item_key_name == "min_repro_dist_factor": display_value_str = f"{val_to_display:.1f}x CELL_SIZE"


        label_surface=self.small_font.render(f"{text_label}: {display_value_str}",True,BLACK)
        surface.blit(label_surface,(self.menu_panel_rect.x+20,y_position))
        
        if not isinstance(val_to_display, tuple) and not is_dict_val:
            if item_key_name == "cinematic_mode_default_on":
                toggle_button_rect = pygame.Rect(self.menu_panel_rect.x + self.menu_panel_rect.width - 120, y_position, 100, 30)
                self._draw_button(surface, "Toggle", toggle_button_rect, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.small_font)
                self.menu_item_rects[f"{item_key_name}_toggle"] = toggle_button_rect
            else:
                minus_text_surf,plus_text_surf=self.font.render("-",True,BLACK),self.font.render("+",True,BLACK)
                button_x_start = self.menu_panel_rect.x + self.menu_panel_rect.width - 100
                minus_button_rect=pygame.Rect(button_x_start, y_position, 30, 30) 
                plus_button_rect=pygame.Rect(button_x_start + 50, y_position, 30, 30)
                
                pygame.draw.rect(surface,LIGHT_GRAY,minus_button_rect,border_radius=5)
                pygame.draw.rect(surface,LIGHT_GRAY,plus_button_rect,border_radius=5)
                surface.blit(minus_text_surf,(minus_button_rect.x+10,minus_button_rect.y+5))
                surface.blit(plus_text_surf,(plus_button_rect.x+10,plus_button_rect.y+5))
                
                action_key_base = f"{item_key_name}"
                if is_dict_val and dict_key:
                    action_key_base += f"_{dict_key}"

                self.menu_item_rects[f"{action_key_base}_minus"] = minus_button_rect
                self.menu_item_rects[f"{action_key_base}_plus"] = plus_button_rect
        return y_position+35 
    
    def _draw_settings_screen_or_menu(self, is_pre_game):
        panel_width,panel_height=700, SETTINGS["screen_height"] - 60 
        self.menu_panel_rect=pygame.Rect((SETTINGS["screen_width"]-panel_width)/2,(SETTINGS["screen_height"]-panel_height)/2,panel_width,panel_height)
        
        if is_pre_game: self.screen.fill(LIGHT_GRAY) 
        else: 
            overlay_surface=pygame.Surface(self.screen.get_size(),pygame.SRCALPHA)
            overlay_surface.fill((0,0,0,128));self.screen.blit(overlay_surface,(0,0))
        
        pygame.draw.rect(self.screen,WHITE,self.menu_panel_rect,border_radius=10)
        pygame.draw.rect(self.screen,BLACK,self.menu_panel_rect,2,border_radius=10)
        
        title_text = "Settings" if is_pre_game else "Settings (M or Esc to Close)"
        title_surface=self.font.render(title_text,True,BLACK)
        self.screen.blit(title_surface,(self.menu_panel_rect.x+(panel_width-title_surface.get_width())/2,self.menu_panel_rect.y+15))
        
        tab_y_start = self.menu_panel_rect.y + 50
        tab_x_start = self.menu_panel_rect.x + 10
        
        self.settings_page_buttons.clear()
        
        current_tab_x = tab_x_start
        current_tab_y = tab_y_start
        max_tab_width_per_row = panel_width - 20 

        for cat_name in SETTINGS_CATEGORIES.keys():
            text_surf = self.small_font.render(cat_name, True, MENU_TEXT_COLOR)
            tab_rect_width = text_surf.get_width() + 20 
            
            if current_tab_x + tab_rect_width > tab_x_start + max_tab_width_per_row and current_tab_x != tab_x_start : 
                current_tab_x = tab_x_start
                current_tab_y += 35 

            tab_rect = pygame.Rect(current_tab_x, current_tab_y, tab_rect_width, 30)
            is_active_tab = cat_name == self.settings_menu_page
            self._draw_button(self.screen, cat_name, tab_rect, 
                              MENU_BUTTON_HOVER_COLOR if is_active_tab else MENU_BUTTON_COLOR, 
                              MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.small_font)
            self.settings_page_buttons[cat_name] = tab_rect
            current_tab_x += tab_rect_width + 2 


        current_y_pos=current_tab_y + 45 
        self.menu_item_rects.clear() 

        items_to_display = SETTINGS_CATEGORIES.get(self.settings_menu_page, [])
        for setting_key in items_to_display:
            if setting_key in SETTINGS:
                current_value = SETTINGS[setting_key]
                is_int = isinstance(current_value, int) or \
                         setting_key in ["gm_spawn", "max_meat", "meat_decay", "world_w", "world_h", 
                                          "ai_stagger", "pop_size", "fps", "overcrowding_limit", 
                                          "green_meat_cluster_max_size", "initial_energy_min", "initial_energy_max",
                                          "energy_gain_meat", "reproduction_cooldown", "genetic_max_energy_min",
                                          "genetic_max_energy_max", "meat_energy_value", "green_meat_energy_value",
                                          "green_meat_spawn_interval", "green_meat_cluster_min_size",
                                          "green_meat_cluster_radius", "spatial_grid_cell_size",
                                          "min_initial_spawn_separation", "target_search_cooldown_min_ms",
                                          "target_search_cooldown_max_ms", "sporadic_move_cooldown_min_ms",
                                          "sporadic_move_cooldown_max_ms", "terrain_chunk_size",
                                          "cinematic_event_lifetime_ms", "cinematic_focus_duration_ms"]


                if isinstance(current_value, dict) or setting_key in ["cell_maintenance_costs", "cinematic_event_interest_scores"]:
                    label_surf = self.small_font.render(f"{setting_key.replace('_',' ').title()}: (Edit in Code)", True, DARK_GRAY)
                    self.screen.blit(label_surf, (self.menu_panel_rect.x + 20, current_y_pos))
                    current_y_pos += 35
                    continue
                
                if setting_key == "cinematic_mode_default_on": 
                     current_y_pos=self._draw_menu_item(self.screen, "Cinematic Mode", SETTINGS["cinematic_mode_default_on"], current_y_pos, "cinematic_mode_default_on")
                elif isinstance(current_value, tuple):
                    display_str = f"{setting_key.replace('_',' ').title()}: {str(current_value)}"
                    label_surf = self.small_font.render(display_str, True, BLACK)
                    self.screen.blit(label_surf, (self.menu_panel_rect.x + 20, current_y_pos))
                    current_y_pos += 35
                    continue
                else:
                    current_y_pos=self._draw_menu_item(self.screen, setting_key.replace("_", " ").title(), 
                                                    current_value, current_y_pos, setting_key, is_integer=is_int)
                
                if current_y_pos > self.menu_panel_rect.bottom - 110: 
                    break 
        
        # Draw Step Multiplier Buttons
        multiplier_y_pos = self.menu_panel_rect.bottom - 75 
        multiplier_texts = ["x1", "x10", "x100", "x1000"] 
        multiplier_values = [0.1, 10.0, 100.0, 1000.0]   
        mult_button_width = 60
        
        total_mult_buttons_width = len(multiplier_texts) * mult_button_width + (len(multiplier_texts) -1) * 5
        mult_current_x = self.menu_panel_rect.x + (self.menu_panel_rect.width - total_mult_buttons_width) / 2


        self.multiplier_button_rects.clear()

        step_label_surf = self.small_font.render("Step Multiplier:", True, BLACK)
        label_x_pos = self.menu_panel_rect.x + 20 
        
        self.screen.blit(step_label_surf, (label_x_pos, multiplier_y_pos + 5))


        for i, text in enumerate(multiplier_texts):
            rect = pygame.Rect(mult_current_x, multiplier_y_pos, mult_button_width, 30)
            base_color = MENU_BUTTON_HOVER_COLOR if self.settings_step_multiplier == multiplier_values[i] else MENU_BUTTON_COLOR
            self._draw_button(self.screen, text, rect, base_color, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.small_font)
            self.multiplier_button_rects[text] = (rect, multiplier_values[i]) 
            mult_current_x += mult_button_width + 5
        
        if is_pre_game:
            # Add Import/Export buttons only in pre-game settings for now
            io_button_y = self.menu_panel_rect.bottom - 45
            export_rect = pygame.Rect(self.menu_panel_rect.x + 20, io_button_y, 150, 30)
            import_rect = pygame.Rect(self.menu_panel_rect.x + 180, io_button_y, 150, 30)
            self._draw_button(self.screen, "Export Settings", export_rect, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.small_font)
            self._draw_button(self.screen, "Import Settings", import_rect, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.small_font)
            self.menu_item_rects["export_settings"] = export_rect
            self.menu_item_rects["import_settings"] = import_rect

            back_button_rect = pygame.Rect(self.menu_panel_rect.right - 120, io_button_y, 100, 30) 
            self._draw_button(self.screen, "Back", back_button_rect, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_TEXT_COLOR, self.font)
            self.menu_item_rects["back_to_main_menu"] = back_button_rect 

        pygame.display.flip()


    def _handle_menu_item_click(self,mouse_pos): 
        # Check multiplier buttons first
        for mult_text, (rect, mult_val) in self.multiplier_button_rects.items():
            if rect.collidepoint(mouse_pos):
                self.settings_step_multiplier = mult_val
                return 

        for item_key_action, rect_obj in self.menu_item_rects.items():
            if rect_obj.collidepoint(mouse_pos):
                if item_key_action == "back_to_main_menu": 
                    self.game_state = STATE_MAIN_MENU
                    return
                if item_key_action == "export_settings": 
                    self._export_settings()
                    return
                if item_key_action == "import_settings": 
                    self._import_settings()
                    return
                
                if item_key_action == "cinematic_mode_default_on_toggle":
                    self.cinematic_mode_active = not self.cinematic_mode_active
                    SETTINGS["cinematic_mode_default_on"] = self.cinematic_mode_active
                    if not self.cinematic_mode_active and self.camera: 
                        self.camera.target_x, self.camera.target_y = self.camera.x, self.camera.y
                        self.camera.target_zoom = self.camera.zoom
                    return


                item_key, action_type = item_key_action.rsplit('_',1)
                
                if isinstance(SETTINGS.get(item_key), tuple):
                    continue

                base_step = 0.1 
                is_int_setting = isinstance(SETTINGS.get(item_key), int) or \
                                 item_key in ["gm_spawn", "max_meat", "meat_decay", "world_w", "world_h", 
                                              "ai_stagger", "pop_size", "fps", "overcrowding_limit", 
                                              "green_meat_cluster_max_size", "initial_energy_min", "initial_energy_max",
                                              "energy_gain_meat", "reproduction_cooldown", "genetic_max_energy_min",
                                              "genetic_max_energy_max", "meat_energy_value", "green_meat_energy_value",
                                              "green_meat_spawn_interval", "green_meat_cluster_min_size",
                                              "green_meat_cluster_radius", "spatial_grid_cell_size",
                                              "min_initial_spawn_separation", "target_search_cooldown_min_ms",
                                              "target_search_cooldown_max_ms", "sporadic_move_cooldown_min_ms",
                                              "sporadic_move_cooldown_max_ms", "terrain_chunk_size",
                                              "cinematic_event_lifetime_ms", "cinematic_focus_duration_ms"] 
                if is_int_setting: base_step = 1

                # Define base steps for settings
                if item_key == "gm_spawn": base_step = 500
                elif item_key == "atk_drain": base_step = 0.5 
                elif item_key == "mut_rate": base_step = 0.005 
                elif item_key == "atk_range": base_step = CELL_SIZE * 0.25 
                elif item_key == "movement_cost_rate_per_velocity": base_step = 0.05 
                elif item_key == "pop_size": base_step = 10 
                elif item_key == "min_repro_dist_factor": base_step = 0.1 
                elif item_key == "world_w" or item_key == "world_h": base_step = 200 
                elif item_key == "ai_stagger": base_step = 1
                elif item_key == "max_meat": base_step = 100 
                elif item_key == "meat_decay": base_step = 20000 
                elif item_key == "fps": base_step = 10
                elif item_key == "overcrowding_limit": base_step = 1
                elif item_key == "green_meat_cluster_max_size": base_step = 1
                elif item_key == "initial_energy_min" or item_key == "initial_energy_max": base_step = 50
                elif item_key == "energy_gain_meat": base_step = 10
                elif item_key == "reproduction_cooldown": base_step = 500
                elif item_key == "target_search_cooldown_min_ms" or item_key == "target_search_cooldown_max_ms": base_step = 50
                elif item_key == "sporadic_move_cooldown_min_ms" or item_key == "sporadic_move_cooldown_max_ms": base_step = 100
                elif item_key == "cinematic_focus_duration_ms": base_step = 500
                
                actual_step = base_step * self.settings_step_multiplier


                current_val = SETTINGS.get(item_key)
                if item_key == "min_repro_dist_factor": 
                    current_val = SETTINGS["min_reproduction_distance"] / CELL_SIZE

                if current_val is None: continue 

                new_val = current_val + actual_step if action_type=="plus" else current_val - actual_step

                if item_key == "time_rate": SETTINGS["default_time_rate"]=clamp(new_val,SETTINGS["time_slider_min"],SETTINGS["time_slider_max"]); self.time_rate=SETTINGS["default_time_rate"]
                elif item_key == "gm_spawn": SETTINGS["green_meat_spawn_interval"]=max(100,int(new_val))
                elif item_key == "atk_drain": SETTINGS["energy_drain_per_attack_cell_per_second"]=max(0,new_val)
                elif item_key == "mut_rate": SETTINGS["mutation_rate_default"]=clamp(new_val,0.0,0.5)
                elif item_key == "atk_range": SETTINGS["attack_range_bonus"]=max(0,new_val)
                elif item_key == "movement_cost_rate_per_velocity": SETTINGS["movement_cost_rate_per_velocity"]=max(0.0001,new_val) 
                elif item_key == "pop_size": SETTINGS["population_size"]=max(1,int(new_val))
                elif item_key == "min_repro_dist_factor": SETTINGS["min_reproduction_distance"] = max(CELL_SIZE * 0.1, new_val * CELL_SIZE)
                elif item_key == "world_w": SETTINGS["world_width"] = max(SETTINGS["screen_width"], int(new_val)) 
                elif item_key == "world_h": SETTINGS["world_height"] = max(SETTINGS["screen_height"], int(new_val))
                elif item_key == "ai_stagger": SETTINGS["ai_update_stagger_factor"] = max(1, int(new_val))
                elif item_key == "max_meat": SETTINGS["max_total_meat_items"] = max(10, int(new_val))
                elif item_key == "meat_decay": SETTINGS["meat_decay_time"] = max(5000, int(new_val))
                elif item_key == "fps": SETTINGS["fps"] = max(10, int(new_val))
                elif item_key == "overcrowding_limit": SETTINGS["overcrowding_limit"] = max(1, int(new_val))
                elif item_key == "green_meat_cluster_max_size": SETTINGS["green_meat_cluster_max_size"] = max(1, int(new_val))
                elif item_key == "cinematic_focus_duration_ms": SETTINGS["cinematic_focus_duration_ms"] = max(500, int(new_val))
                else: 
                    if is_int_setting : SETTINGS[item_key] = int(new_val)
                    else: SETTINGS[item_key] = new_val 
                break 
    
    def _get_serializable_settings(self):
        """Returns a copy of SETTINGS with non-serializable items removed."""
        serializable = {}
        for key, value in SETTINGS.items():
            if not isinstance(value, pygame.Rect): # Filter out pygame.Rect
                serializable[key] = value
        return serializable

    def _export_settings(self):
        try:
            serializable_settings = self._get_serializable_settings()
            settings_json = json.dumps(serializable_settings, indent=4)
            encoded_settings = base64.b64encode(settings_json.encode('utf-8')).decode('utf-8')
            print("\n--- Settings Export ---")
            print("Copy the following string to import these settings later:")
            print(encoded_settings)
            print("-----------------------\n")
            # For a real UI, you'd put this in a selectable text box or copy to clipboard
        except Exception as e:
            print(f"Error exporting settings: {e}")

    def _import_settings(self):
        print("\n--- Settings Import ---")
        encoded_string = input("Paste the exported settings string here and press Enter: ")
        try:
            decoded_json = base64.b64decode(encoded_string.encode('utf-8')).decode('utf-8')
            loaded_settings = json.loads(decoded_json)
            
            for key, value in loaded_settings.items():
                if key in SETTINGS:
                    # Basic type checking to prevent major issues
                    if isinstance(SETTINGS[key], type(value)) or \
                       (isinstance(SETTINGS[key], (int, float)) and isinstance(value, (int, float))):
                        SETTINGS[key] = value
                    elif key == "time_slider_rect": # Don't overwrite this specific Rect
                        pass 
                    else:
                        print(f"Warning: Type mismatch for setting '{key}'. Skipping.")
                else:
                    print(f"Warning: Unknown setting '{key}' in imported string. Skipping.")
            
            # Re-apply any settings that affect game objects immediately if needed
            self.time_rate = SETTINGS["default_time_rate"]
            if self.world: # If simulation is running, re-init might be too disruptive
                print("Settings imported. Some changes may require a simulation restart to fully apply (e.g., world size, population).")
            else:
                print("Settings imported. They will apply when you start a new simulation.")

        except Exception as e:
            print(f"Error importing settings: {e}. Please ensure the string is correct.")
        print("-----------------------\n")


    def _draw_ui_main(self):
        if self.game_state == STATE_SIMULATION:
            slider_rect=SETTINGS["time_slider_rect"]
            pygame.draw.rect(self.screen,DARK_GRAY,slider_rect);pygame.draw.rect(self.screen,BLACK,slider_rect,2)
            time_range = SETTINGS["time_slider_max"]-SETTINGS["time_slider_min"]
            knob_ratio = (self.time_rate-SETTINGS["time_slider_min"])/time_range if time_range != 0 else 0
            knob_pos_x = slider_rect.x+knob_ratio*slider_rect.width
            knob_rect = pygame.Rect(0,0,10,slider_rect.height+10)
            knob_rect.centery,knob_rect.centerx = slider_rect.centery,knob_pos_x
            pygame.draw.rect(self.screen,BLACK,knob_rect)
            rate_text_surf = self.font.render(f"Time: {self.time_rate:.2f}x",True,BLACK)
            self.screen.blit(rate_text_surf,(slider_rect.right+10,slider_rect.centery-rate_text_surf.get_height()//2))
        
        if self.world: 
            species_count_val=len(self.world.species_list)
            count_text_surf=self.font.render(f"Species: {species_count_val}",True,BLACK)
            self.screen.blit(count_text_surf,(10,10))
        fps_text_surf=self.font.render(f"FPS: {self.clock.get_fps():.1f}",True,BLACK)
        self.screen.blit(fps_text_surf,(10,35))
        
        pygame.draw.rect(self.screen, MENU_BUTTON_COLOR, self.menu_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, MENU_BUTTON_BORDER_COLOR, self.menu_button_rect, 2, border_radius=5)
        self.screen.blit(self.menu_button_text_surface, (self.menu_button_rect.x + 10, self.menu_button_rect.y + 5))

        if self.game_state == STATE_SIMULATION:
            cinematic_text = "Cinematic: ON" if self.cinematic_mode_active else "Cinematic: OFF (C)"
            cinematic_surf = self.small_font.render(cinematic_text, True, BLACK)
            self.screen.blit(cinematic_surf, (SETTINGS["screen_width"] - cinematic_surf.get_width() - 10, self.menu_button_rect.bottom + 5))


    def _update_simulation(self, dt_scaled):
        if not self.world or not self.camera: return

        if self.cinematic_mode_active:
            most_interesting_event = None
            highest_score = -1
            current_time = self.world.simulation_time
            
            if self.cinematic_current_focus_event_id is not None:
                focused_event = next((evt for evt in self.world.event_log if evt["id"] == self.cinematic_current_focus_event_id), None)
                if focused_event and not focused_event.get("viewed_fully", False) and (current_time - focused_event["timestamp"] < SETTINGS["cinematic_event_lifetime_ms"]):
                    self.cinematic_focus_duration_timer += dt_scaled
                    if self.cinematic_focus_duration_timer >= SETTINGS["cinematic_focus_duration_ms"]:
                        focused_event["viewed_fully"] = True
                        self.cinematic_current_focus_event_id = None 
                        self.cinematic_focus_duration_timer = 0
                    else: 
                        self.camera.target_x, self.camera.target_y = focused_event["location"]
                        self.camera.target_zoom = SETTINGS["cinematic_mode_target_zoom"]
                else: 
                    self.cinematic_current_focus_event_id = None
                    self.cinematic_focus_duration_timer = 0
            
            if self.cinematic_current_focus_event_id is None:
                valid_events_for_new_focus = []
                for event in self.world.event_log:
                    age = current_time - event["timestamp"]
                    if age < SETTINGS["cinematic_event_lifetime_ms"] and not event.get("viewed_fully", False):
                        decay_factor = (SETTINGS["cinematic_event_lifetime_ms"] - age) / SETTINGS["cinematic_event_lifetime_ms"]
                        current_interest = event["interest_score"] * decay_factor
                        if current_interest > highest_score:
                            highest_score = current_interest
                            most_interesting_event = event
                        valid_events_for_new_focus.append(event) 
                # self.world.event_log = valid_events_for_new_focus # Optional: more aggressive pruning

                if most_interesting_event:
                    self.cinematic_current_focus_event_id = most_interesting_event["id"]
                    self.cinematic_focus_duration_timer = 0
                    self.camera.target_x, self.camera.target_y = most_interesting_event["location"]
                    self.camera.target_zoom = SETTINGS["cinematic_mode_target_zoom"]
                else: 
                    self.cinematic_pan_timer_ms += dt_scaled
                    if self.cinematic_pan_target_pos is None or self.cinematic_pan_timer_ms >= SETTINGS["cinematic_pan_duration_ms"]:
                        if self.world: 
                            self.cinematic_pan_target_pos = (random.uniform(0, self.world.width), random.uniform(0, self.world.height))
                            self.camera.target_x, self.camera.target_y = self.cinematic_pan_target_pos
                        self.camera.target_zoom = SETTINGS["zoom_initial"] * 0.7 
                        self.cinematic_pan_timer_ms = 0
            
            self.camera.update_cinematic(dt_scaled)
        
        self.world.update(dt_scaled)


    def run(self):
        while self.running:
            dt_milliseconds = self.clock.tick(SETTINGS["fps"])
            
            self._handle_input() 
            
            if self.game_state == STATE_SIMULATION:
                dt_scaled_for_world = 0 if self.settings_menu_active else dt_milliseconds * self.time_rate
                if not self.settings_menu_active: 
                    self._update_simulation(dt_scaled_for_world) 
                
                self.screen.fill(WHITE)
                if self.world and self.camera:
                    self.world.draw_terrain(self.screen,self.camera)
                    self.world.draw_entities(self.screen,self.camera)
                self._draw_ui_main() 
                

            elif self.game_state == STATE_MAIN_MENU:
                self._draw_main_menu()
            
            elif self.game_state == STATE_PRE_GAME_SETTINGS:
                self._draw_settings_screen_or_menu(is_pre_game=True)
            
            elif self.game_state == STATE_IN_GAME_SETTINGS_MENU: 
                self.screen.fill(WHITE)
                if self.world and self.camera:
                    self.world.draw_terrain(self.screen,self.camera)
                    self.world.draw_entities(self.screen,self.camera)
                self._draw_ui_main()
                self._draw_settings_screen_or_menu(is_pre_game=False) 
            
            pygame.display.flip()
        
        pygame.quit() 

if __name__ == "__main__":
    game = Game()
    try:
        game.run() 
    except SystemExit:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
            
    sys.exit()
