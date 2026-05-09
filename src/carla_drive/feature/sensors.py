def spawn_rgb_camera(vehicle, width, height, callback):
    """Spawn and attach an RGB camera to a CARLA vehicle.

    Args:
        vehicle: CARLA vehicle actor to attach the camera to
        width: Image width in pixels
        height: Image height in pixels
        callback: Function to call with each frame (receives numpy array)
    """
    import carla

    # Get world and blueprint
    world = vehicle.get_world()
    blueprint_library = world.get_blueprint_library()
    blueprint = blueprint_library.find('sensor.camera.rgb')

    # Configure camera dimensions
    blueprint.set_attribute('image_size_x', str(width))
    blueprint.set_attribute('image_size_y', str(height))

    # TODO: Spawn and attach camera
    # TODO: Setup callback