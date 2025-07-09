from PIL import Image

# 选择高质量的重采样滤镜（Pillow ≥ 9.1）
resample_filter = Image.Resampling.LANCZOS

filenames = ["button_normal.png", "button_hover.png", "button_press.png"]

for fn in filenames:
    img = Image.open(fn)
    img = img.resize((70, 70), resample=resample_filter)
    out_name = fn.replace(".png", "_70x70.png")
    img.save(out_name, format="PNG")
    print(f"Saved: {out_name}")
