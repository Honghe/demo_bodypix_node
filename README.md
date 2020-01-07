# BodyPix on Node.js
Segmented by BodyPix 2.0 and visualized by Python.
![](./screenshots/bodypix1.png)

## Usage

### Directory tree
```
├── demo                # `root_dir` 
│   ├── demo_mask.mp4   # step 4 output
│   ├── demo.mp4        # origin input
│   ├── jpgs            # step 1 output
│   ├── jsons           # stpe 2 output
│   └── masked_jpgs     # step 3 output
```

### 5 steps
- step 0
Make a directory as `root_dir`, and put a .mp4 file to your `root_dir`. 
The .mp4 file name must be the same as your `root_dir`, e.g. a `demo.mp4` in `demo` directory.

- step 1
```
python3 1_mp4_to_jpgs.py `root_dir`
```

- step 2
```
node main.js `root_dir`
```

- step 3
```
python3 utils/visualization.py `root_dir`
```

- step 4
```
python3 4_jpgs_to_mp4.py `root_dir`
```