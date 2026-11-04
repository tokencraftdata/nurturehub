import { integer, sqliteTable, text } from 'drizzle-orm/sqlite-core';
export const mealProfiles = sqliteTable('meal_profiles', { id: integer('id').primaryKey(), preferences: text('preferences').notNull(), daysJson: text('days_json').notNull(), updatedAt: text('updated_at').notNull() });
export const familyProfiles = sqliteTable('family_profiles', { userId: text('user_id').primaryKey(), dataJson: text('data_json').notNull(), updatedAt: text('updated_at').notNull() });
