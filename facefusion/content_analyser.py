from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

from facefusion import state_manager
from facefusion.types import DownloadScope, DownloadSet, ExecutionProvider, Fps, ModelSet, VisionFrame

STREAM_COUNTER = 0


def create_static_model_set(download_scope : DownloadScope) -> ModelSet:
	"""
	NSFW detection models have been removed from this fork. Keep the public API so
	dependent modules do not break, but return an empty model set.
	"""
	return {}


def collect_model_downloads() -> Tuple[DownloadSet, DownloadSet]:
	"""
	Previously returned hash/source dictionaries for NSFW ONNX weights.
	Now both dictionaries are empty so the download manager has nothing to fetch.
	"""
	return {}, {}


def get_inference_pool() -> Dict[str, Any]:
	return {}


def clear_inference_pool() -> None:
	return None


def resolve_execution_providers() -> List[ExecutionProvider]:
	"""
	Defer to the global execution providers so the inference manager behaves normally
	even though no sessions are created.
	"""
	return state_manager.get_item('execution_providers')


def pre_check() -> bool:
	"""
	With the NSFW pipeline removed there is nothing to validate, so we always succeed.
	"""
	return True


def analyse_stream(vision_frame : Optional[VisionFrame], video_fps : Fps) -> bool:
	global STREAM_COUNTER
	STREAM_COUNTER += 1
	return False


def analyse_frame(vision_frame : Optional[VisionFrame]) -> bool:
	return False


@lru_cache()
def analyse_image(image_path : str) -> bool:
	return False


@lru_cache()
def analyse_video(video_path : str, trim_frame_start : int, trim_frame_end : int) -> bool:
	return False
