"""Test basic import of sensors module."""
import inspect


def test_import_spawn_rgb_camera():
    """Test that spawn_rgb_camera can be imported."""
    from carla_drive.feature.sensors import spawn_rgb_camera

    assert callable(spawn_rgb_camera)


def test_spawn_rgb_camera_signature():
    """Test that spawn_rgb_camera has the expected signature."""
    from carla_drive.feature.sensors import spawn_rgb_camera

    sig = inspect.signature(spawn_rgb_camera)
    params = list(sig.parameters.keys())

    assert params == ['vehicle', 'width', 'height', 'callback']