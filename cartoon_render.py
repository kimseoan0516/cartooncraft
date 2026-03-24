import cv2
import numpy as np
import argparse
import os


def _ensure_positive_odd(value: int, name: str) -> int:
    """Ensure a parameter is a positive odd integer."""
    if value <= 0 or value % 2 == 0:
        raise ValueError(f"{name} must be a positive odd integer, got {value}")
    return value


def cartoon_render(img: np.ndarray,
                   bilateral_d: int = 9,
                   bilateral_sigma_color: float = 300,
                   bilateral_sigma_space: float = 300,
                   bilateral_iters: int = 3,
                   median_ksize: int = 7,
                   adaptive_block_size: int = 9,
                   adaptive_c: float = 2) -> np.ndarray:
    """
    Convert an image to cartoon style using bilateral filtering + edge detection.

    Parameters
    ----------
    img                  : Input BGR image (numpy array)
    bilateral_d          : Diameter of each pixel neighbourhood for bilateral filter
    bilateral_sigma_color: Filter sigma in color space
    bilateral_sigma_space: Filter sigma in coordinate space
    bilateral_iters      : Number of times bilateral filter is applied
    median_ksize         : Kernel size for median blur (noise reduction)
    adaptive_block_size  : Block size for adaptive thresholding (must be odd)
    adaptive_c           : Constant subtracted from mean in adaptive threshold

    Returns
    -------
    cartoon : Cartoon-stylized BGR image
    """
    # ── 1. Smooth colors while preserving edges (bilateral filter) ──────────
    color = img.copy()
    for _ in range(bilateral_iters):
        color = cv2.bilateralFilter(color,
                                    d=bilateral_d,
                                    sigmaColor=bilateral_sigma_color,
                                    sigmaSpace=bilateral_sigma_space)

    # ── 2. Build an edge mask from the grayscale version ────────────────────
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, median_ksize)          # reduce noise first
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY,
                                  adaptive_block_size,
                                  adaptive_c)

    # ── 3. Combine smooth color with dark edges ──────────────────────────────
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon


def process_image(input_path: str, output_path: str, **kwargs) -> None:
    """Load an image, apply cartoon rendering, and save the result."""
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {input_path}")

    cartoon = cartoon_render(img, **kwargs)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, cartoon)
    print(f"Saved → {output_path}")


def save_side_by_side(input_path: str, output_path: str, comparison_path: str) -> None:
    """Save a horizontal comparison image (original | cartoon)."""
    original = cv2.imread(input_path)
    cartoon = cv2.imread(output_path)
    if original is None or cartoon is None:
        raise FileNotFoundError("Cannot build comparison image. Check input/output paths.")

    if original.shape[:2] != cartoon.shape[:2]:
        cartoon = cv2.resize(cartoon, (original.shape[1], original.shape[0]))

    comparison = np.hstack([original, cartoon])
    os.makedirs(os.path.dirname(os.path.abspath(comparison_path)), exist_ok=True)
    cv2.imwrite(comparison_path, comparison)
    print(f"Saved comparison → {comparison_path}")


def _default_output_paths(input_path: str) -> tuple[str, str]:
    """Build simple default output filenames from input filename."""
    input_dir = os.path.dirname(os.path.abspath(input_path))
    stem = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(input_dir, f"{stem}_cartoon.jpg")
    comparison_path = os.path.join(input_dir, f"{stem}_compare.jpg")
    return output_path, comparison_path


def main():
    parser = argparse.ArgumentParser(
        description="Cartoon Rendering using OpenCV bilateral filter + adaptive thresholding"
    )
    parser.add_argument("input",  help="Path to input image")
    parser.add_argument(
        "output",
        nargs="?",
        default="",
        help="Optional output cartoon path (default: <input>_cartoon.jpg)"
    )
    parser.add_argument("--bilateral_d",           type=int,   default=9)
    parser.add_argument("--bilateral_sigma_color", type=float, default=300)
    parser.add_argument("--bilateral_sigma_space", type=float, default=300)
    parser.add_argument("--bilateral_iters",       type=int,   default=3)
    parser.add_argument("--median_ksize",          type=int,   default=7)
    parser.add_argument("--adaptive_block_size",   type=int,   default=9)
    parser.add_argument("--adaptive_c",            type=float, default=2)
    parser.add_argument(
        "--comparison",
        type=str,
        default="",
        help="Optional comparison path. Use 'auto' for <input>_compare.jpg"
    )
    args = parser.parse_args()

    args.median_ksize = _ensure_positive_odd(args.median_ksize, "median_ksize")
    args.adaptive_block_size = _ensure_positive_odd(args.adaptive_block_size, "adaptive_block_size")
    default_output, default_comparison = _default_output_paths(args.input)
    output_path = args.output if args.output else default_output

    process_image(
        args.input, output_path,
        bilateral_d=args.bilateral_d,
        bilateral_sigma_color=args.bilateral_sigma_color,
        bilateral_sigma_space=args.bilateral_sigma_space,
        bilateral_iters=args.bilateral_iters,
        median_ksize=args.median_ksize,
        adaptive_block_size=args.adaptive_block_size,
        adaptive_c=args.adaptive_c,
    )

    if args.comparison:
        comparison_path = default_comparison if args.comparison.lower() == "auto" else args.comparison
        save_side_by_side(args.input, output_path, comparison_path)


if __name__ == "__main__":
    main()
