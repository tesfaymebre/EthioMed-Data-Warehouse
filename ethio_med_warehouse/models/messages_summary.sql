-- models/intermediate/messages_summary.sql
SELECT
    channel_title,
    message_date,
    COUNT(message_id) AS total_messages,
    COUNT(media_path) AS total_media,
    COUNT(DISTINCT channel_username) AS unique_channels
FROM {{ ref('stg_telegram_messages') }} GROUP BY channel_title, message_date
