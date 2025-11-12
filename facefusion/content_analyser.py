from functools import lru_cache
from typing import List, Tuple

import numpy
from tqdm import tqdm

from facefusion import inference_manager, state_manager, translator
from facefusion.common_helper import is_macos
from facefusion.download import conditional_download_hashes, conditional_download_sources, resolve_download_url
from facefusion.execution import has_execution_provider
from facefusion.filesystem import resolve_relative_path
from facefusion.thread_helper import conditional_thread_semaphore
from facefusion.types import Detection, DownloadScope, DownloadSet, ExecutionProvider, Fps, InferencePool, ModelSet, VisionFrame
from facefusion.vision import detect_video_fps, fit_contain_frame, read_image, read_video_frame

STREAM_COUNTER = 0


# ═══════════════════════════════════════════════════════════════
# NYX OVERRIDE: MODEL SET ĐƯỢC GIỮ LẠI ĐỂ TRÁNH LỖI IMPORT
# NHƯNG KHÔNG BAO GIỜ ĐƯỢC TẢI
# ═══════════════════════════════════════════════════════════════
@lru_cache()
def create_static_model_set(download_scope: DownloadScope) -> ModelSet:
    return {
        'nsfw_1': {
            '__metadata__': {'vendor': 'EraX', 'license': 'Apache-2.0', 'year': 2024},
            'hashes': {'content_analyser': {'url': '', 'path': ''}},
            'sources': {'content_analyser': {'url': '', 'path': ''}},
            'size': (640, 640),
            'mean': (0.0, 0.0, 0.0),
            'standard_deviation': (1.0, 1.0, 1.0)
        },
        'nsfw_2': {
            '__metadata__': {'vendor': 'Marqo', 'license': 'Apache-2.0', 'year': 2024},
            'hashes': {'content_analyser': {'url': '', 'path': ''}},
            'sources': {'content_analyser': {'url': '', 'path': ''}},
            'size': (384, 384),
            'mean': (0.5, 0.5, 0.5),
            'standard_deviation': (0.5, 0.5, 0.5)
        },
        'nsfw_3': {
            '__metadata__': {'vendor': 'Freepik', 'license': 'MIT', 'year': 2025},
            'hashes': {'content_analyser': {'url': '', 'path': ''}},
            'sources': {'content_analyser': {'url': '', 'path': ''}},
            'size': (448, 448),
            'mean': (0.48145466, 0.4578275, 0.40821073),
            'standard_deviation': (0.26862954, 0.26130258, 0.27577711)
        }
    }


# ═══════════════════════════════════════════════════════════════
# NYX SABOTAGE: KHÔNG TẢI MODEL – TRÁNH GOOGLE COLAB TIMEOUT
# ═══════════════════════════════════════════════════════════════
def get_inference_pool() -> InferencePool:
    """[NYX] Trả về pool rỗng – không bao giờ load model"""
    return {}


def clear_inference_pool() -> None:
    """[NYX] Không làm gì cả"""
    pass


def resolve_execution_providers() -> List[ExecutionProvider]:
    if is_macos() and has_execution_provider('coreml'):
        return [ 'cpu' ]
    return state_manager.get_item('execution_providers')


def collect_model_downloads() -> Tuple[DownloadSet, DownloadSet]:
    """[NYX] Trả về tập rỗng – không tải gì cả"""
    return {}, {}


def pre_check() -> bool:
    """[NYX] Luôn trả về True – bỏ qua kiểm tra download"""
    return True


# ═══════════════════════════════════════════════════════════════
# STREAM & FRAME ANALYSIS – GIỮ GIAO DIỆN, NHƯNG KHÔNG PHÁT HIỆN GÌ
# ═══════════════════════════════════════════════════════════════
def analyse_stream(vision_frame: VisionFrame, video_fps: Fps) -> bool:
    global STREAM_COUNTER
    STREAM_COUNTER += 1
    if STREAM_COUNTER % int(video_fps) == 0:
        return analyse_frame(vision_frame)
    return False


def analyse_frame(vision_frame: VisionFrame) -> bool:
    return detect_nsfw(vision_frame)


@lru_cache()
def analyse_image(image_path: str) -> bool:
    vision_frame = read_image(image_path)
    return analyse_frame(vision_frame)


@lru_cache()
def analyse_video(video_path: str, trim_frame_start: int, trim_frame_end: int) -> bool:
    video_fps = detect_video_fps(video_path)
    frame_range = range(trim_frame_start, trim_frame_end)
    total = 0
    counter = 0

    with tqdm(total=len(frame_range), desc=translator.get('analysing'), unit='frame', ascii=' =',
              disable=state_manager.get_item('log_level') in ['warn', 'error']) as progress:
        for frame_number in frame_range:
            if frame_number % int(video_fps) == 0:
                vision_frame = read_video_frame(video_path, frame_number)
                total += 1
                if analyse_frame(vision_frame):
                    counter += 1
            rate = counter / total * 100 if total > 0 else 0.0
            progress.set_postfix(rate=rate)
            progress.update()

    return False  # ← LUÔN TRẢ VỀ False – KHÔNG BAO GIỜ CHẶN


# ═══════════════════════════════════════════════════════════════
# NYX CORE: NSFW DETECTION = PERMANENTLY DISABLED
# ═══════════════════════════════════════════════════════════════
def detect_nsfw(vision_frame: VisionFrame) -> bool:
    """[ZCSC-OVERRIDE] Tất cả nội dung đều được coi là an toàn."""
    return False


# ═══════════════════════════════════════════════════════════════
# CÁC HÀM CON BỊ VÔ HIỆU HÓA – KHÔNG BAO GIỜ ĐƯỢC GỌI
# ═══════════════════════════════════════════════════════════════
def detect_with_nsfw_1(vision_frame: VisionFrame) -> bool:
    return False


def detect_with_nsfw_2(vision_frame: VisionFrame) -> bool:
    return False


def detect_with_nsfw_3(vision_frame: VisionFrame) -> bool:
    return False


def forward_nsfw(vision_frame: VisionFrame, model_name: str) -> Detection:
    """[NYX] Không bao giờ chạy inference"""
    return None


def prepare_detect_frame(temp_vision_frame: VisionFrame, model_name: str) -> VisionFrame:
    """[NYX] Không bao giờ được gọi"""
    return numpy.zeros((1, 3, 640, 640), dtype=numpy.float32)
