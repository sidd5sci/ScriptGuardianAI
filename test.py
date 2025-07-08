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



# samba 
# https://sambanova.ai/lp/ai-api-key?utm_source=google&utm_medium=cpc&utm_campaign=&utm_term=free%20ai%20api&utm_content=&hsa_acc=9878570407&hsa_cam=22694290306&hsa_grp=178095958941&hsa_ad=759134360539&hsa_src=g&hsa_tgt=kwd-566653825169&hsa_kw=free%20ai%20api&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gad_campaignid=22694290306&gbraid=0AAAAABZUQ-FO2WiLdP58imvuJdnC_6B3z&gclid=CjwKCAjwmenCBhA4EiwAtVjzmtR39vs4TAHw0dCX1Mj3j7uyZAIUdvTCUQHb8CT3OgKyDHi6xAa6SxoCzgkQAvD_BwE
# 60b25fd9-d338-42e3-b21d-db5678b35c48

# curl -H "Authorization: Bearer $API_KEY" \
#      -H "Content-Type: application/json" \
#      -d '{
# 	"stream": true,
# 	"model": "DeepSeek-R1-Distill-Llama-70B",
# 	"messages": [
# 		{
# 			"role": "system",
# 			"content": "You are a helpful assistant"
# 		},
# 		{
# 			"role": "user",
# 			"content": "Hello"
# 		}
# 	]
# 	}' \
#      -X POST https://api.sambanova.ai/v1/chat/completions


# data: {"choices":[{"delta":{"content":"\u003cthink\u003e","role":"assistant"},"finish_reason":null,"...

# curl -H "Authorization: Bearer <your-api-key>" \
#      -H "Content-Type: application/json" \
#      -d '{
# 	"stream": true,
# 	"model": "DeepSeek-R1-0528",
# 	"messages": [
# 		{
# 			"role": "system",
# 			"content": "You are a helpful assistant"
# 		},
# 		{
# 			"role": "user",
# 			"content": "Hello"
# 		}
# 	]
# 	}' \
#      -X POST https://api.sambanova.ai/v1/chat/completions