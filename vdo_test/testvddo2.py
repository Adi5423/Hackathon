import moviepy.editor as moviepy

# List of image file paths (e.g., '1.png', '2.png', etc.)
image_files = ['12.png', '13.png', '14.png', '15.png']

# Create a video clip from the images
clip = moviepy.ImageSequenceClip(image_files,.1)

# Write the video to an MP4 file
clip.write_videofile("output.mp4", fps=24)
