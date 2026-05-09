"""Test basic import of sensors module."""


def test_import_spawn_rgb_camera():
    """Test that spawn_rgb_camera can be imported."""
    from carla_drive.feature.sensors import spawn_rgb_camera

    assert callable(spawn_rgb_camera)