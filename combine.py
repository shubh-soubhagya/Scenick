import cv2
import numpy as np
import mediapipe as mp

def remove_bg(image):
    """
    Removes background using MediaPipe Selfie Segmentation.
    Returns RGBA image (512x512) with transparent background.
    """
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_seg:
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = selfie_seg.process(rgb_img)
        mask = results.segmentation_mask > 0.5

        # Create RGBA
        output = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
        output[mask] = np.concatenate(
            (image[mask], np.full((np.sum(mask), 1), 255, dtype=np.uint8)), axis=1
        )
        return output

def overlay_same_size(background_img, char_img_rgba):
    """
    Overlays a transparent character image over a same-size background image.
    """
    # Ensure both are same size (512x512)
    if background_img.shape[:2] != char_img_rgba.shape[:2]:
        raise ValueError("Images must be same size")

    # Convert background to BGRA if needed
    if background_img.shape[2] == 3:
        background_img = cv2.cvtColor(background_img, cv2.COLOR_BGR2BGRA)

    alpha_char = char_img_rgba[:, :, 3] / 255.0
    alpha_bg = 1.0 - alpha_char

    for c in range(0, 3):
        background_img[:, :, c] = (
            alpha_char * char_img_rgba[:, :, c] +
            alpha_bg * background_img[:, :, c]
        )

    return background_img

# if __name__ == "__main__":
#     # Load images (512x512)
#     bg_img = cv2.imread(r"generated_images\background_img.png")
#     char_img = cv2.imread(r"generated_images\char_img.png")

#     # Remove background
#     char_img_rgba = remove_bg(char_img)

#     # Overlay
#     final_img = overlay_same_size(bg_img, char_img_rgba)

#     # Save and show
#     cv2.imwrite("combined_result.png", final_img)
#     cv2.imshow("Combined", final_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
