/**
 * Validation schemas and types for authentication forms
 * Using Yup for form validation with Formik
 */

import * as Yup from "yup";

// ============================================================================
// Type Definitions
// ============================================================================

export interface LoginFormValues {
  email: string;
  password: string;
}

export interface RegisterFormValues {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface TaskFormValues {
  title: string;
  description: string;
  deadline: string;
  priority: "low" | "medium" | "high" | "urgent";
}

// ============================================================================
// Yup Validation Schemas
// ============================================================================

/**
 * Validation schema for login form
 * Requirements:
 * - email: valid email format
 * - password: at least 6 characters
 */
export const loginValidationSchema = Yup.object().shape({
  email: Yup.string()
    .email("Please enter a valid email address")
    .required("Email is required")
    .trim(),
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required"),
});

/**
 * Validation schema for registration form
 * Requirements:
 * - name: required, at least 2 characters
 * - email: valid email format
 * - password: at least 8 characters
 * - confirmPassword: must match password
 */
export const registerValidationSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Name must be at least 2 characters")
    .max(50, "Name must not exceed 50 characters")
    .required("Name is required")
    .trim(),
  email: Yup.string()
    .email("Please enter a valid email address")
    .required("Email is required")
    .trim(),
  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      "Password must contain at least one uppercase letter, one lowercase letter, and one number"
    )
    .required("Password is required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password")], "Passwords must match")
    .required("Please confirm your password"),
});

/**
 * Validation schema for task creation form
 * Requirements:
 * - title: required, at least 3 characters
 * - description: optional
 * - deadline: optional, must be a valid date
 * - priority: required, must be one of the valid priority levels
 */
export const taskValidationSchema = Yup.object().shape({
  title: Yup.string()
    .min(3, "Task title must be at least 3 characters")
    .max(500, "Task title must not exceed 500 characters")
    .required("Task title is required")
    .trim(),
  description: Yup.string()
    .max(5000, "Description must not exceed 5000 characters")
    .trim(),
  deadline: Yup.string()
    .typeError("Deadline must be a valid date")
    .nullable(),
  priority: Yup.string()
    .oneOf(["low", "medium", "high", "urgent"], "Invalid priority level")
    .required("Priority is required"),
});
