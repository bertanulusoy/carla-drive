"""Test RGB camera configuration."""

from unittest.mock import Mock
import sys


def test_rgb_camera_blueprint_configuration():
    """Test that RGB camera blueprint is configured with correct dimensions."""
    # Mock carla module
    mock_carla = Mock()
    sys.modules["carla"] = mock_carla

    try:
        from carla_drive.feature.sensors import spawn_rgb_camera

        # Mock the CARLA objects
        mock_world = Mock()
        mock_blueprint_library = Mock()
        mock_blueprint = Mock()
        mock_vehicle = Mock()
        mock_camera = Mock()

        # Setup blueprint library
        mock_world.get_blueprint_library.return_value = mock_blueprint_library
        mock_blueprint_library.find.return_value = mock_blueprint

        # Mock vehicle world
        mock_vehicle.get_world.return_value = mock_world

        # Mock spawn_actor
        mock_world.spawn_actor.return_value = mock_camera

        # Call the function (it will fail later, but we test config part)
        try:
            spawn_rgb_camera(mock_vehicle, 640, 480, lambda x: None)
        except Exception:
            pass  # Expected to fail without full setup

        # Verify blueprint was found
        mock_blueprint_library.find.assert_called_with("sensor.camera.rgb")

        # Verify attributes were set
        mock_blueprint.set_attribute.assert_any_call("image_size_x", "640")
        mock_blueprint.set_attribute.assert_any_call("image_size_y", "480")

        # Verify camera was spawned with correct transform and attachment
        mock_world.spawn_actor.assert_called_once()
        call_args = mock_world.spawn_actor.call_args
        assert call_args[0][0] == mock_blueprint  # blueprint
        assert call_args[1]["attach_to"] == mock_vehicle  # attach_to

        # Check that transform was created (detailed checks would require more mocking)

    finally:
        # Clean up
        if "carla" in sys.modules:
            del sys.modules["carla"]
