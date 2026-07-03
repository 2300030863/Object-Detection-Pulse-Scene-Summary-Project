# Smart Scene Understanding Architecture

```mermaid
flowchart TD
    A[User Input<br/>Image / Video / Camera Frame] --> B[CLI Detection Script]
    B --> C[YOLOv11 Object Detection<br/>Ultralytics + PyTorch]
    C --> D[Detected Objects List]
    C --> E[Annotated Media Output]
    D --> F{Engine}
    F -->|basic| G[Rule-Based Scene Summary<br/>SceneSummarizer]
    F -->|blip| H[BLIP Caption Generation<br/>Salesforce/blip-image-captioning-base]
    H --> I[Caption Text]
    I --> J[Text Summarization<br/>Transformers pipeline]
    J --> K[Short Scene Summary]
    G --> K
    E --> L[OpenCV Window / Saved Output]
    D --> L
    I --> L
    K --> L
```

## Runtime Flow

1. User runs image/video/camera script and provides input media.
2. YOLOv11 detects objects and generates annotated output.
3. If engine is `blip`, BLIP produces a scene caption.
4. Caption is summarized into a short scene summary.
5. Output displays detected objects, caption, and summary in CLI/visual output.
