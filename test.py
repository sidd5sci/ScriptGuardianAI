import torch
import os
from diffusers import CogVideoXImageToVideoPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image

# Step 1: Load the pipeline
print("⏳ Loading CogVideoX model...")
pipe = CogVideoXImageToVideoPipeline.from_pretrained(
    "THUDM/CogVideoX-5b-I2V", 
    torch_dtype=torch.bfloat16
)
pipe.to("cpu")  # Change to "cuda" if using GPU
print("✅ Model loaded.")

# Step 2: Load the input image
print("🖼️ Loading image...")
image = load_image("/Users/siddhartha.singh/my_projects/AI projects/test/rt82_zyqx_220416.jpg")
print("✅ Image loaded.")

# Step 3: Generate video frames
print("🎬 Generating video frames (this might take a few minutes)...")
result = pipe(prompt="A cartoon tank in war zone", image=image, num_frames=4, guidance_scale=3)
print("✅ Video frames generated.")
video_frames = result.frames
print(f"✅ {len(video_frames)} frames generated.")

# Step 4: Save video
print("💾 Saving video as MP4...")
export_to_video(video_frames, "output_video.mp4", fps=8)
print("✅ Video saved as output_video.mp4.")

# Step 5: Save each frame as image
frames_folder = "frames"
os.makedirs(frames_folder, exist_ok=True)

print(f"📸 Saving each frame to ./{frames_folder}/ ...")
for idx, frame in enumerate(video_frames):
    frame.save(os.path.join(frames_folder, f"frame_{idx:03d}.png"))
print(f"✅ All frames saved in '{frames_folder}' folder.")

