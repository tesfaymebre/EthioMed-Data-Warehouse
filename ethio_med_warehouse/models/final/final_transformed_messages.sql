-- models/final/final_transformed_messages.sql
SELECT
    channel_title,
    message_date::DATE AS message_day,
    SUM(total_messages) AS total_messages,
    SUM(total_media) AS total_media
FROM {{ ref('messages_summary') }}
GROUP BY channel_title, message_day
ORDER BY channel_title, message_day
