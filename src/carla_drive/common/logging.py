get_logger(name: str)


from carla_drive.common.logging import get_logger
log = get_logger(carla_drive)
log.info("app_started", mode="dev")

