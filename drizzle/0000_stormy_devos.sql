CREATE TABLE `meal_profiles` (
	`id` integer PRIMARY KEY NOT NULL,
	`preferences` text NOT NULL,
	`days_json` text NOT NULL,
	`updated_at` text NOT NULL
);
