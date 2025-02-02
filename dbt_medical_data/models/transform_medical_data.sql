-- models/transform_medical_data.sql

{{ config(materialized='table') }}

WITH processed_data AS (
    SELECT
        message_id,
        channel_title,
        channel_username,
        message,
        CASE
            WHEN message ~ '^[A-Za-z ]+' THEN  -- Checks if the message starts with letters (product name)
                TRIM(SUBSTRING(message FROM '^(.*?)\s+'))  -- Extracts product name until the first space
            ELSE NULL
        END AS product_name,
        CASE
            WHEN message ~ '\s[0-9]+\s?[A-Za-z]*' THEN  -- Checks if a number followed by text (optional) appears in the message
                TRIM(SUBSTRING(message FROM '\s([0-9]+\s?[A-Za-z]*)'))  -- Extracts the number and possible text after
            ELSE NULL
        END AS usage_info,
        cast(message_date as timestamp) as message_date,  -- Ensure message_date is in timestamp format
        emoji_used,
        youtube_links
    FROM {{ ref('medical_source_data') }}
)

SELECT 
    message_id,
    channel_title,
    channel_username,
    message,
    product_name,
    usage_info,
    message_date,
    emoji_used,
    youtube_links
FROM processed_data
WHERE product_name IS NOT NULL OR usage_info IS NOT NULL