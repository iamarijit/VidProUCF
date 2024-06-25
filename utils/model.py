from transformers import MaskFormerFeatureExtractor, MaskFormerForInstanceSegmentation
from transformers import ViTFeatureExtractor, ViTForImageClassification


def get_models():
    segment_feature_extractor = MaskFormerFeatureExtractor.from_pretrained("facebook/maskformer-swin-tiny-coco")
    segment_model = MaskFormerForInstanceSegmentation.from_pretrained("facebook/maskformer-swin-tiny-coco")

    gender_feature_extractor = ViTFeatureExtractor.from_pretrained('rizvandwiki/gender-classification')
    gender_model = ViTForImageClassification.from_pretrained('rizvandwiki/gender-classification')

    return segment_feature_extractor, segment_model, gender_feature_extractor, gender_model

def get_segmentation_labels(frame, feature_extractor, model):
    id2label = model.config.id2label

    inputs = feature_extractor(images=frame, return_tensors="pt")
    outputs = model(**inputs)

    result = feature_extractor.post_process_panoptic_segmentation(outputs, target_sizes=[frame.shape[:2]])[0]
    labels = [id2label[i['label_id']] for i in result["segments_info"]]
    return labels

def get_gender(frame, feature_extractor, model):
    id2label = model.config.id2label

    inputs = feature_extractor(images=frame, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits

    predicted_class_idx = logits.argmax(-1).item()
    gender = id2label[predicted_class_idx]
    return gender.title()


def detect_human_presence(segment_labels, human_label='person'):
    return human_label in segment_labels

def detect_location(
        segment_labels, 
        outdoor_labels=[
            'building-other-merged', 'tree-merged', 
            'grass-merged', 'sky-other-merged', 
            'river', 'road']
    ):
    for label in outdoor_labels:
        if label in segment_labels:
            return 'Outdoor'
    return 'Indoor'

def extract_model_info(
        key_frames,
        segment_feature_extractor, 
        segment_model, 
        gender_feature_extractor, 
        gender_model
    ):
    is_human_present = False
    genders = []

    for frame in key_frames:
        segment_labels = get_segmentation_labels(frame, segment_feature_extractor, segment_model)
        is_human_present = detect_human_presence(segment_labels)

        if is_human_present:
            gender = get_gender(frame, gender_feature_extractor, gender_model)
            genders.append(gender)

    location = detect_location(segment_labels)
    return is_human_present, set(genders), location