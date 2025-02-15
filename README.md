## Player data

Template for project repo, including set up of project sprint boards and issues

## Definition Done:

-   Code Completeness

Code is fully written and adheres to team coding standards.
The feature branch passes all automated tests (unit, integration, and performance tests).
Testing

Unit tests cover at least 80% of the codebase for the specific task.
Integration tests validate that the ETL app components work seamlessly together.
Manual testing has been conducted, and edge cases have been reviewed.

-   Functionality

The feature meets the requirements outlined in the task description.
ETL scripts can extract data from the specified source, transform it as per the rules, and load it into the correct destination.
Performance benchmarks for data processing are met (e.g., process X rows in under Y seconds).

-   Documentation

Code is properly documented with clear comments explaining non-obvious logic.
The task includes updates to project documentation (e.g., README.md, API documentation).

The Git issue is updated with a clear summary of the changes made.

---

## **Project Overview**

### **Problem Statement**

The conversation around the greatest football player has been had for decades, with new players emerging from every generation making their claim to thrown. However, a comprehensive take on this question using data has not been conducted before. How can we use data to answer this question?

### **Solution**

This project builds a robust ETL pipeline to:

-   Collect transaction data from web sources of player data.
-   Transform raw data to align with a predefined metrics.
-   Load the transformed data into a seperate script that will then analyse the data.
-   Visualize and analyze data using Python.

---

## **Architecture**

### **Technologies Used**

-   **Grafana**: For visualizing and analyzing data.
-   **Python**: For the ETL pipeline logic.
-   **Docker**: For local development and testing.

### **Pipeline Steps**

1. **Data Extraction**

    - Web scraping and saving data to a new CSV file.

2. **Data Transformation**

    - Parse and clean raw data to align with the predefined metrics, only taking on the relevent data we need.
    - Remove unused data such as team accolades.
    - Normalize data

3. **Data Loading**

    - Load transformed data into a new Python script where it can be analysed.

4. **Data Visualization**
    - Connect Redshift to Grafana to enable query-based dashboards and insights.

---

## **How to Deploy the Pipeline**

### **Prerequisites**

-   Python 3.9 or later.

### **Deployment Steps**

---

---

## **Sample Queries**

### **List All Branches**


---

## **Future Enhancements**


---

## **Acknowledgments**


