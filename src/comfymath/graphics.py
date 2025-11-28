from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence, Tuple


SDXL_SUPPORTED_RESOLUTIONS = [
    (1024, 1024, 1.0),
    (1152, 896, 1.2857142857142858),
    (896, 1152, 0.7777777777777778),
    (1216, 832, 1.4615384615384615),
    (832, 1216, 0.6842105263157895),
    (1344, 768, 1.75),
    (768, 1344, 0.5714285714285714),
    (1536, 640, 2.4),
    (640, 1536, 0.4166666666666667),
]

SDXL_EXTENDED_RESOLUTIONS = [
    (512, 2048, 0.25),
    (512, 1984, 0.26),
    (512, 1920, 0.27),
    (512, 1856, 0.28),
    (576, 1792, 0.32),
    (576, 1728, 0.33),
    (576, 1664, 0.35),
    (640, 1600, 0.4),
    (640, 1536, 0.42),
    (704, 1472, 0.48),
    (704, 1408, 0.5),
    (704, 1344, 0.52),
    (768, 1344, 0.57),
    (768, 1280, 0.6),
    (832, 1216, 0.68),
    (832, 1152, 0.72),
    (896, 1152, 0.78),
    (896, 1088, 0.82),
    (960, 1088, 0.88),
    (960, 1024, 0.94),
    (1024, 1024, 1.0),
    (1024, 960, 1.8),
    (1088, 960, 1.14),
    (1088, 896, 1.22),
    (1152, 896, 1.30),
    (1152, 832, 1.39),
    (1216, 832, 1.47),
    (1280, 768, 1.68),
    (1344, 768, 1.76),
    (1408, 704, 2.0),
    (1472, 704, 2.10),
    (1536, 640, 2.4),
    (1600, 640, 2.5),
    (1664, 576, 2.90),
    (1728, 576, 3.0),
    (1792, 576, 3.12),
    (1856, 512, 3.63),
    (1920, 512, 3.76),
    (1984, 512, 3.89),
    (2048, 512, 4.0),
]


QWEN_SUPPORTED_RESOLUTIONS = [
    (1328, 1328, 1.0),
    (1664, 928, 1.793103448275862),
    (928, 1664, 0.5576923076923077),
    (1472, 1140, 1.2912280701754386),
    (1140, 1472, 0.7744565217391305),
    (1584, 1056, 1.5),
    (1056, 1584, 0.6666666666666666),
]


Z_IMAGE_RESOLUTIONS_1024 = [
    (1024, 1024, 1.0),
    (1152, 896, 1.2857142857142858),
    (896, 1152, 0.7777777777777778),
    (1152, 864, 1.3333333333333333),
    (864, 1152, 0.75),
    (1248, 832, 1.5),
    (832, 1248, 0.6666666666666666),
    (1280, 720, 1.7777777777777777),
    (720, 1280, 0.5625),
    (1344, 576, 2.3333333333333335),
    (576, 1344, 0.42857142857142855),
]


Z_IMAGE_RESOLUTIONS_1280 = [
    (1280, 1280, 1.0),
    (1440, 1120, 1.2857142857142858),
    (1120, 1440, 0.7777777777777778),
    (1472, 1104, 1.3333333333333333),
    (1104, 1472, 0.75),
    (1536, 1024, 1.5),
    (1024, 1536, 0.6666666666666666),
    (1600, 896, 1.7857142857142858),
    (896, 1600, 0.56),
    (1680, 720, 2.3333333333333335),
    (720, 1680, 0.42857142857142855),
]


class Resolution(ABC):
    @classmethod
    @abstractmethod
    def resolutions(cls) -> Sequence[Tuple[int, int, float]]: ...

    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "resolution": ([f"{res[0]}x{res[1]}" for res in cls.resolutions()],)
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "op"
    CATEGORY = "math/graphics"

    def op(self, resolution: str) -> tuple[int, int]:
        width, height = resolution.split("x")
        return (int(width), int(height))


class NearestResolution(ABC):
    @classmethod
    @abstractmethod
    def resolutions(cls) -> Sequence[Tuple[int, int, float]]: ...

    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"image": ("IMAGE",)}}

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "op"
    CATEGORY = "math/graphics"

    def op(self, image) -> tuple[int, int]:
        image_width = image.size()[2]
        image_height = image.size()[1]
        print(f"Input image resolution: {image_width}x{image_height}")
        image_ratio = image_width / image_height
        differences = [
            (abs(image_ratio - resolution[2]), resolution)
            for resolution in self.resolutions()
        ]
        smallest = None
        for difference in differences:
            if smallest is None:
                smallest = difference
            else:
                if difference[0] < smallest[0]:
                    smallest = difference
        if smallest is not None:
            width = smallest[1][0]
            height = smallest[1][1]
        else:
            width = 1024
            height = 1024
        print(f"Selected resolution: {width}x{height}")
        return (width, height)


class SDXLResolution(Resolution):
    @classmethod
    def resolutions(cls):
        return SDXL_SUPPORTED_RESOLUTIONS


class SDXLExtendedResolution(Resolution):
    @classmethod
    def resolutions(cls):
        return SDXL_EXTENDED_RESOLUTIONS


class NearestSDXLResolution(NearestResolution):
    @classmethod
    def resolutions(cls):
        return SDXL_SUPPORTED_RESOLUTIONS


class NearestSDXLExtendedResolution(NearestResolution):
    @classmethod
    def resolutions(cls):
        return SDXL_EXTENDED_RESOLUTIONS


class QwenResolution(Resolution):
    @classmethod
    def resolutions(cls):
        return QWEN_SUPPORTED_RESOLUTIONS


class NearestQwenResolution(NearestResolution):
    @classmethod
    def resolutions(cls):
        return QWEN_SUPPORTED_RESOLUTIONS


class ZImage1024Resolution(Resolution):
    @classmethod
    def resolutions(cls):
        return Z_IMAGE_RESOLUTIONS_1024


class NearestZImage1024Resolution(NearestResolution):
    @classmethod
    def resolutions(cls):
        return Z_IMAGE_RESOLUTIONS_1024


class ZImage1280Resolution(Resolution):
    @classmethod
    def resolutions(cls):
        return Z_IMAGE_RESOLUTIONS_1280


class NearestZImage1280Resolution(NearestResolution):
    @classmethod
    def resolutions(cls):
        return Z_IMAGE_RESOLUTIONS_1280


NODE_CLASS_MAPPINGS = {
    "CM_SDXLResolution": SDXLResolution,
    "CM_NearestSDXLResolution": NearestSDXLResolution,
    "CM_SDXLExtendedResolution": SDXLExtendedResolution,
    "CM_NearestSDXLExtendedResolution": NearestSDXLExtendedResolution,
    "CM_QwenResolution": QwenResolution,
    "CM_NearestQwenResolution": NearestQwenResolution,
    "CM_ZImage1024Resolution": ZImage1024Resolution,
    "CM_NearestZImage1024Resolution": NearestZImage1024Resolution,
    "CM_ZImage1280Resolution": ZImage1280Resolution,
    "CM_NearestZImage1280Resolution": NearestZImage1280Resolution,
}
