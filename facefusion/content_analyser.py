from functools import lru_cache
from typing import Any, Dict, Tuple

from facefusion.types import DownloadScope, DownloadSet, Fps, ModelSet, VisionFrame

STREAM_COUNTER = 0


def create_static_model_set(download_scope : DownloadScope) -> ModelSet:
	"""
	FaceFusion previously shipped NSFW detection models. This fork removes them entirely,
	so the static model set is empty but the public API stays intact.
	"""
	return {}


def collect_model_downloads() -> Tuple[DownloadSet, DownloadSet]:
	"""
	Keep compatibility with the download manager while signalling that there is nothing to fetch.
	"""
	return {}, {}


def get_inference_pool() -> Dict[str, Any]:
	return {}


def clear_inference_pool() -> None:
	return None


def pre_check() -> bool:
	"""
	Without NSFW models there is nothing to validate, so always succeed.
	"""
	return True


def analyse_stream(vision_frame : VisionFrame, video_fps : Fps) -> bool:
	global STREAM_COUNTER
	STREAM_COUNTER += 1
	return False


def analyse_frame(vision_frame : VisionFrame) -> bool:
	return False


@lru_cache()
def analyse_image(image_path : str) -> bool:
	return False


@lru_cache()
def analyse_video(video_path : str, trim_frame_start : int, trim_frame_end : int) -> bool:
	return False
