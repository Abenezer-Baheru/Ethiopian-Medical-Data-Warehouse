{{ config(materialized='table') }}

select *
from {{ source('public', 'telegram_medical_messages') }}