def spawn_rgb_camera(vehicle, width, height, callback):
    """Spawn and attach an RGB camera to a CARLA vehicle.

    Args:
        vehicle: CARLA vehicle actor to attach the camera to
        width: Image width in pixels
        height: Image height in pixels
        callback: Function to call with each frame (receives numpy array)
    """
    import carla

    pass