# Face-Recognition
Mitigating the Impact of Attribute Editing on Face Recognition

Code

    -- Attribute: folder contains code for calculating the accuracy of BLIP & LLava attribute detection
        -- Attribute results
            -- result_blip: BLIP score of whether an attribute is present in the image or not
            -- result_llava: LLaVa score of whether an attribute is present in the image or not
            -- original: original score

    -- LLava: folder contains code for LLaVa benchmarking on different result images

    -- t-SNE: folder contains code for generating t-SNE plots for various combinations of attributes & image results

    -- InstantID: code for generating InstantID images

Result_InstantID

    -- result images generated using InstantID
        
TSNE results

    -- tsne: regular & transformed plots separately comparing similar attributes for BLIP, InstantID, and DreamBooth images
    
    -- tsne_attributes: plots for each attribute containing BLIP, InstantID, and DreamBooth images
    
    -- tsne_attributes2: plots for each attribute containing BLIP, InstantID, and CN-IP images

References:

InstantID code is sourced from https://github.com/InstantID/InstantID. infer_full.py files are updated according to the required prompts; the rest of the method remains the same.
