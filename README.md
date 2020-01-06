# BodyPix on Node.js
Segmented by BodyPix 2.0 and visualized by Python.
![](./screenshots/bodypix1.png)

## Usage
**Notice**
You have to modify `root_dir` in each step.

### Directory tree
```
├── `root_dir`
│   ├── demo_mask.mp4   # step 4 output
│   ├── demo.mp4        # origin input
│   ├── jpgs            # step 1 output
│   ├── jsons           # stpe 2 output
│   └── masked_jpgs     # step 3 output
```

### 4 steps

- step1
```
python3 1_mp4_to_jpgs.py
```

- step2
```
npm run main
```

- step3
```
python3 utils/visualization.py
```

- step4
```
python3 4_jpgs_to_mp4.py
```