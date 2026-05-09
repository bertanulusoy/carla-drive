"""Test RGB camera callback and image processing."""

from unittest.mock import Mock
import sys
import numpy as np


def test_rgb_camera_callback_processes_image():
    """Test that camera callback converts image data to numpy array."""
    # Mock carla module
    mock_carla = Mock()
    sys.modules["carla"] = mock_carla

    try:
        from carla_drive.feature.sensors import spawn_rgb_camera

        # Mock objects
        mock_world = Mock()
        mock_blueprint_library = Mock()
        mock_blueprint = Mock()
        mock_vehicle = Mock()
        mock_camera = Mock()

        # Setup mocks
        mock_world.get_blueprint_library.return_value = mock_blueprint_library
        mock_blueprint_library.find.return_value = mock_blueprint
        mock_vehicle.get_world.return_value = mock_world
        mock_world.spawn_actor.return_value = mock_camera

        # Track callback calls
        callback_calls = []

        def mock_callback(image_array):
            callback_calls.append(image_array)

        # Call spawn function
        spawn_rgb_camera(mock_vehicle, 640, 480, mock_callback)

        # Verify camera.listen was called
        mock_camera.listen.assert_called_once()

        # Get the callback function that was passed to listen
        listen_callback = mock_camera.listen.call_args[0][0]

        # Create mock image with raw data
        mock_image = Mock()
        # Simulate BGRA data: 640*480*4 bytes
        raw_data = np.random.randint(0, 256, (640 * 480 * 4), dtype=np.uint8)
        mock_image.raw_data = raw_data.tobytes()

        # Call the processing callback
        listen_callback(mock_image)

        # Verify callback was called with numpy array
        assert len(callback_calls) == 1
        image_array = callback_calls[0]

        # Verify it's a numpy array
        assert isinstance(image_array, np.ndarray)

        # Verify shape is (height, width, 3) for RGB
        assert image_array.shape == (480, 640, 3)

        # Verify dtype is uint8
        assert image_array.dtype == np.uint8

    finally:
        # Clean up
        if "carla" in sys.modules:
            del sys.modules["carla"]
