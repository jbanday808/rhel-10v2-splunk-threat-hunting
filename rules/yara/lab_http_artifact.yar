rule LAB_Synthetic_HTTP_Artifact
{
    meta:
        description = "Identifies the two inert markers in the synthetic HTTP exercise"
        purpose = "training fixture only"

    strings:
        $review_marker = "LAB_REVIEW_MARKER" ascii
        $artifact_marker = "LAB_SYNTHETIC_HTTP_ARTIFACT" ascii

    condition:
        filesize < 1KB and all of them
}
