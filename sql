SELECT
    SUM(CASE WHEN 'Admin' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Admin",
    SUM(CASE WHEN 'Super Admin' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Super Admin",
    SUM(CASE WHEN 'Manager' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Manager",
    SUM(CASE WHEN 'Viewers' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Viewers"
FROM user_details;
