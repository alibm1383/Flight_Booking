# Test Report

*Report generated on 16-Jul-2026 at 15:33:21 by [pytest-md]*

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

37 tests ran in 4.87 seconds

- 37 passed

## 37 passed

### Safari_Backend\app\tests\test_auth.py

`test_register_customer_success` 0.08s

`test_register_airline_success` 0.07s

`test_register_without_optional_email` 0.06s

`test_register_duplicate_phone_number` 0.06s

`test_login_success` 0.12s

`test_login_wrong_password` 0.13s

`test_login_non_existent_user` 0.00s

`test_login_inactive_user` 0.13s

`test_register_invalid_password_length` 0.00s

`test_register_invalid_phone_format` 0.01s

`test_register_invalid_email_format` 0.01s

### Safari_Backend\app\tests\test_profile.py

`test_get_my_information` 0.08s

`test_update_customer_profile_success` 0.07s

`test_update_airline_profile_success` 0.07s

`test_update_admin_profile_success` 0.07s

`test_update_customer_wrong_role` 0.07s

`test_update_profile_phone_number_success` 0.07s

`test_update_profile_phone_duplicate` 0.13s

`test_update_profile_phone_invalid_format` 0.08s

`test_update_profile_duplicate_email` 0.14s

`test_change_password_success_and_wrong_current` 0.23s

`test_change_password_mismatch` 0.05s

`test_upload_avatar_success` 0.06s

`test_upload_avatar_invalid_format` 0.05s

`test_remove_avatar_success` 0.06s

`test_remove_avatar_not_found` 0.05s

### Safari_Backend\app\tests\test_users.py

`test_rbac_non_admin_access_denied` 0.01s

`test_get_customers_pagination` 0.02s

`test_invalid_pagination_params` 0.01s

`test_get_airlines_pagination` 0.01s

`test_search_customers` 0.01s

`test_search_airlines` 0.01s

`test_get_customer_detail_success_and_not_found` 0.01s

`test_get_airline_detail` 0.01s

`test_toggle_user_status_success` 0.01s

`test_admin_cannot_block_himself` 0.01s

`test_toggle_status_user_not_found` 0.01s
