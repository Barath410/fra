-- SEED DATA for VanAdhikar Drishti Database
-- Generated: 2026-02-23
-- Users: 5 | Villages: 10 | Claims: 15 | Officers: 5 | Grievances: 5

USE fra_documents;

-- ============================================================================
-- 1. USERS (5 records)
-- ============================================================================
INSERT INTO users (email, name, picture, provider, last_login) VALUES
('ramesh.bhil@fra.gov.in', 'Ramesh Kumar Bhil', 'https://api.example.com/pic/user1.jpg', 'google', NOW()),
('priya.venkatesh@fra.gov.in', 'Priya Venkatesh', 'https://api.example.com/pic/user2.jpg', 'google', NOW() - INTERVAL 2 DAY),
('vikram.singh@fra.gov.in', 'Vikram Singh', 'https://api.example.com/pic/user3.jpg', 'google', NOW() - INTERVAL 5 DAY),
('geeta.sharma@fra.gov.in', 'Geeta Sharma', 'https://api.example.com/pic/user4.jpg', 'google', NOW() - INTERVAL 1 DAY),
('anil.patel@fra.gov.in', 'Anil Patel', NULL, 'google', NOW() - INTERVAL 10 DAY);

-- ============================================================================
-- 2. OFFICERS (5 records)
-- ============================================================================
INSERT INTO officers (officer_id, name, designation, state, district, block, mobile, email, last_active) VALUES
('OFF-MP-2024-001', 'Dr. Ashok Verma', 'District Forest Officer', 'MP', 'Mandla', 'Mandla', '+91-9876543210', 'ashok.verma@forestry.gov.in', NOW()),
('OFF-MP-2024-002', 'Suresh Kumar', 'Range Officer', 'MP', 'Mandla', 'Mawai', '+91-9876543211', 'suresh.kumar@forestry.gov.in', NOW() - INTERVAL 1 DAY),
('OFF-MP-2024-003', 'Rajesh Tiwari', 'SDO (SDLC)', 'MP', 'Mandla', 'Mandla', '+91-9876543212', 'rajesh.tiwari@forest.mp.gov.in', NOW()),
('OFF-CG-2024-001', 'Meena Singh', 'District Manager', 'CG', 'Bastar', 'Bastar', '+91-9876543213', 'meena.singh@cg-tribal.gov.in', NOW() - INTERVAL 3 DAY),
('OFF-MH-2024-001', 'Harish Deshmukh', 'Nodal Officer', 'MH', 'Gadchiroli', 'Gadchiroli', '+91-9876543214', 'harish.deshmukh@mh-fra.gov.in', NOW() - INTERVAL 2 DAY);

-- ============================================================================
-- 3. VILLAGES (10 records)
-- ============================================================================
INSERT INTO villages (code, name, gram_panchayat, block, district, state, population, st_population, total_households, pvtg_present, tribal_groups, total_claims, granted_claims, pending_claims, ifr_granted_area, cfr_granted_area, saturation_score, gps_lat, gps_lng) VALUES
('VIL-MP-MAN-001', 'Bichhiya', 'Bichhiya', 'Mandla', 'Mandla', 'MP', 3450, 2890, 620, FALSE, JSON_ARRAY('Gond', 'Korku'), 8, 5, 2, 45.50, 12.30, 65, 22.6050, 80.3850),
('VIL-MP-MAN-002', 'Narsing Garh', 'Narsing Garh', 'Mandla', 'Mandla', 'MP', 2150, 1890, 380, FALSE, JSON_ARRAY('Gond'), 5, 3, 1, 28.75, 8.50, 48, 22.5950, 80.4050),
('VIL-MP-MAN-003', 'Majhgaon', 'Majhgaon', 'Mawai', 'Mandla', 'MP', 1780, 1560, 310, TRUE, JSON_ARRAY('Baiga', 'Gond'), 6, 4, 2, 32.00, 15.20, 55, 22.7150, 80.2650),
('VIL-MP-MAN-004', 'Mundi', 'Mundi', 'Mawai', 'Mandla', 'MP', 4200, 3750, 745, FALSE, JSON_ARRAY('Gond', 'Korku', 'Baiga'), 12, 8, 3, 58.90, 22.40, 72, 22.7250, 80.2750),
('VIL-MP-MAN-005', 'Bankhedi', 'Bankhedi', 'Mandla', 'Mandla', 'MP', 985, 850, 165, FALSE, JSON_ARRAY('Gond'), 3, 2, 1, 18.50, 6.30, 38, 22.6350, 80.3450),
('VIL-CG-BAS-001', 'Dantewada', 'Dantewada', 'Bastar', 'Bastar', 'CG', 5600, 5100, 980, TRUE, JSON_ARRAY('Bhumij', 'Muria Gond'), 18, 11, 5, 85.60, 35.80, 78, 19.4569, 81.9450),
('VIL-CG-BAS-002', 'Jagdalpur', 'Jagdalpur', 'Bastar', 'Bastar', 'CG', 2340, 1950, 420, FALSE, JSON_ARRAY('Gond'), 7, 4, 2, 42.10, 18.90, 52, 19.5550, 82.0050),
('VIL-MH-GAD-001', 'Melghat', 'Melghat', 'Gadchiroli', 'Gadchiroli', 'MH', 3120, 2800, 560, TRUE, JSON_ARRAY('Warli', 'Gond'), 9, 6, 2, 51.20, 24.50, 68, 21.2050, 76.4450),
('VIL-MP-BAL-001', 'Chopra', 'Chopra', 'Baihar', 'Balaghat', 'MP', 1650, 1420, 295, FALSE, JSON_ARRAY('Baiga', 'Gond'), 5, 3, 1, 28.30, 11.50, 45, 22.0650, 80.2850),
('VIL-MP-BAL-002', 'Lanji', 'Lanji', 'Kirnapur', 'Balaghat', 'MP', 2890, 2450, 515, FALSE, JSON_ARRAY('Gond', 'Korku'), 8, 5, 2, 46.50, 19.80, 62, 22.1250, 80.1550);

-- ============================================================================
-- 4. CLAIMS (15 records)
-- ============================================================================
INSERT INTO claims (claim_id, claimant_name, claimant_aadhaar, village_name, village_code, gram_panchayat, block, district, state, claim_type, area_acres, claim_date, status, tribal_group, is_pvtg, gps_lat, gps_lng, assigned_officer_id) VALUES
('FRA-2026-MP-00001', 'Ramesh Kumar Bhil', '123456789012', 'Bichhiya', 'VIL-MP-MAN-001', 'Bichhiya', 'Mandla', 'Mandla', 'MP', 'IFR', 2.45, '2025-11-15', 'APPROVED', 'Gond', FALSE, 22.6050, 80.3850, 'OFF-MP-2024-001'),
('FRA-2026-MP-00002', 'Geeta Devi', '987654321098', 'Bichhiya', 'VIL-MP-MAN-001', 'Bichhiya', 'Mandla', 'Mandla', 'MP', 'CFR', 5.50, '2025-10-20', 'APPROVED', 'Gond', FALSE, 22.6070, 80.3870, 'OFF-MP-2024-002'),
('FRA-2026-MP-00003', 'Prakash Kumar', '111222333444', 'Narsing Garh', 'VIL-MP-MAN-002', 'Narsing Garh', 'Mandla', 'Mandla', 'MP', 'IFR', 1.88, '2025-11-01', 'PENDING', 'Gond', FALSE, 22.5950, 80.4050, 'OFF-MP-2024-001'),
('FRA-2026-MP-00004', 'Savitri Bai', '555666777888', 'Majhgaon', 'VIL-MP-MAN-003', 'Majhgaon', 'Mawai', 'Mandla', 'MP', 'IFR', 3.25, '2025-09-15', 'APPROVED', 'Baiga', TRUE, 22.7150, 80.2650, 'OFF-MP-2024-002'),
('FRA-2026-MP-00005', 'Mohan Singh', '999888777666', 'Mundi', 'VIL-MP-MAN-004', 'Mundi', 'Mawai', 'Mandla', 'MP', 'CFR', 8.75, '2025-08-30', 'REJECTED', 'Korku', FALSE, 22.7250, 80.2750, NULL),
('FRA-2026-MP-00006', 'Anita Desai', '444555666777', 'Bankhedi', 'VIL-MP-MAN-005', 'Bankhedi', 'Mandla', 'Mandla', 'MP', 'IFR', 1.50, '2025-11-10', 'PENDING', 'Gond', FALSE, 22.6350, 80.3450, 'OFF-MP-2024-001'),
('FRA-2026-CG-00001', 'Lakhan Singh', '666777888999', 'Dantewada', 'VIL-CG-BAS-001', 'Dantewada', 'Bastar', 'Bastar', 'CG', 'CFR', 12.50, '2025-07-22', 'APPROVED', 'Muria Gond', TRUE, 19.4569, 81.9450, 'OFF-CG-2024-001'),
('FRA-2026-CG-00002', 'Priya Deshmukh', '888999111222', 'Dantewada', 'VIL-CG-BAS-001', 'Dantewada', 'Bastar', 'Bastar', 'CG', 'IFR', 4.30, '2025-10-05', 'PENDING', 'Bhumij', FALSE, 19.4580, 81.9460, 'OFF-CG-2024-001'),
('FRA-2026-CG-00003', 'Vikram Roy', '222333444555', 'Jagdalpur', 'VIL-CG-BAS-002', 'Jagdalpur', 'Bastar', 'Bastar', 'CG', 'IFR', 2.75, '2025-11-01', 'APPROVED', 'Gond', FALSE, 19.5550, 82.0050, 'OFF-CG-2024-001'),
('FRA-2026-MH-00001', 'Ashok Marathi', '333444555666', 'Melghat', 'VIL-MH-GAD-001', 'Melghat', 'Gadchiroli', 'Gadchiroli', 'MH', 'CFR', 6.80, '2025-09-10', 'APPROVED', 'Warli', TRUE, 21.2050, 76.4450, 'OFF-MH-2024-001'),
('FRA-2026-MH-00002', 'Savina Rao', '777888999111', 'Melghat', 'VIL-MH-GAD-001', 'Melghat', 'Gadchiroli', 'Gadchiroli', 'MH', 'IFR', 3.15, '2025-08-25', 'PENDING', 'Gond', FALSE, 21.2080, 76.4480, 'OFF-MH-2024-001'),
('FRA-2026-MP-00007', 'Rajendra Pal', '111333555777', 'Chopra', 'VIL-MP-BAL-001', 'Chopra', 'Baihar', 'Balaghat', 'MP', 'IFR', 2.00, '2025-11-08', 'PENDING', 'Baiga', FALSE, 22.0650, 80.2850, 'OFF-MP-2024-003'),
('FRA-2026-MP-00008', 'Sunita Kewat', '222444666888', 'Lanji', 'VIL-MP-BAL-002', 'Lanji', 'Kirnapur', 'Balaghat', 'MP', 'CFR', 7.20, '2025-10-12', 'APPROVED', 'Korku', FALSE, 22.1250, 80.1550, 'OFF-MP-2024-003'),
('FRA-2026-MP-00009', 'Hari Lal', '444666888222', 'Narsing Garh', 'VIL-MP-MAN-002', 'Narsing Garh', 'Mandla', 'Mandla', 'MP', 'IFR', 1.65, '2025-10-28', 'APPROVED', 'Gond', FALSE, 22.5960, 80.4060, 'OFF-MP-2024-002'),
('FRA-2026-CG-00004', 'Sangeeta Singh', '555777999111', 'Dantewada', 'VIL-CG-BAS-001', 'Dantewada', 'Bastar', 'Bastar', 'CG', 'IFR', 3.90, '2025-11-05', 'PENDING', 'Muria Gond', FALSE, 19.4590, 81.9470, 'OFF-CG-2024-001');

-- ============================================================================
-- 5. GRIEVANCES (5 records)
-- ============================================================================
INSERT INTO grievances (grievance_id, claimant_name, claim_id, village_name, block, district, state, category, status, priority, description, filed_date, assigned_officer_id, source, channel, mobile) VALUES
('GRV-2026-MP-00001', 'Ramesh Kumar Bhil', 'FRA-2026-MP-00001', 'Bichhiya', 'Mandla', 'Mandla', 'MP', 'Slow Processing', 'OPEN', 'HIGH', 'Claim pending for 6 months without update', '2025-11-15', 'OFF-MP-2024-001', 'Direct', 'InPerson', '+91-9987654321'),
('GRV-2026-MP-00002', 'Prakash Kumar', 'FRA-2026-MP-00003', 'Narsing Garh', 'Mandla', 'Mandla', 'MP', 'Document Issue', 'RESOLVED', 'MEDIUM', 'Original documents lost, need resubmission', '2025-10-20', 'OFF-MP-2024-002', 'Phone', 'Telephone', '+91-8876543212'),
('GRV-2026-CG-00001', 'Lakhan Singh', 'FRA-2026-CG-00001', 'Dantewada', 'Bastar', 'Bastar', 'CG', 'Boundary Dispute', 'OPEN', 'CRITICAL', 'Neighboring claim overlapping with survey boundary', '2025-11-20', 'OFF-CG-2024-001', 'NGO', 'Email', '+91-7765432198'),
('GRV-2026-MH-00001', 'Ashok Marathi', 'FRA-2026-MH-00001', 'Melghat', 'Gadchiroli', 'Gadchiroli', 'MH', 'Officer Unavailability', 'PENDING', 'HIGH', 'Assigned officer unreachable for verification', '2025-11-18', 'OFF-MH-2024-001', 'Direct', 'InPerson', '+91-9654321087'),
('GRV-2026-MP-00003', 'Sunita Kewat', 'FRA-2026-MP-00008', 'Lanji', 'Kirnapur', 'Balaghat', 'MP', 'Title Deed Delay', 'OPEN', 'MEDIUM', 'Patta certificate not issued despite approval', '2025-11-22', 'OFF-MP-2024-003', 'Phone', 'Telephone', '+91-7654321234');

-- ============================================================================
-- VERIFICATION QUERIES (Run these to confirm seed data)
-- ============================================================================
-- SELECT COUNT(*) as user_count FROM users;
-- SELECT COUNT(*) as village_count FROM villages;
-- SELECT COUNT(*) as claim_count FROM claims;
-- SELECT COUNT(*) as officer_count FROM officers;
-- SELECT COUNT(*) as grievance_count FROM grievances;
-- 
-- SELECT u.name, u.email, COUNT(c.id) as claim_count
-- FROM users u
-- LEFT JOIN claims c ON c.claimant_name LIKE CONCAT('%', u.name, '%')
-- GROUP BY u.id;
--
-- SELECT state, COUNT(*) as total_claims, 
--        SUM(CASE WHEN status='APPROVED' THEN 1 ELSE 0 END) as approved,
--        SUM(CASE WHEN status='PENDING' THEN 1 ELSE 0 END) as pending,
--        SUM(CASE WHEN status='REJECTED' THEN 1 ELSE 0 END) as rejected
-- FROM claims
-- GROUP BY state;
