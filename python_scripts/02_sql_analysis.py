import pandas as pd
import sqlite3

def run_business_queries():
    db_path = "ferry_database.db"
    csv_path = "/Users/yutong/Documents/code/git_test/toronto-ferry-demand-analytics-2015-2026/CSV_for_analysis/toronto-ferry-cleaned_for_tableau.csv"
    
    print("Connecting to the SQLite database...")
    conn = sqlite3.connect(db_path)
    
    print("Loading cleaned dataset into SQL engine...")
    df = pd.read_csv(csv_path)
    df.to_sql('tickets', conn, if_exists='replace', index=False)
    
    queries = {
        "1. WATER TAXI REVENUE LEAK ANALYSIS": """
            SELECT 
                Year,
                Month,
                SUM(Net_Queue_Change) AS Total_Queue_Build,
                ROUND(SUM(CASE WHEN Net_Queue_Change > 20 THEN Net_Queue_Change * 0.15 ELSE 0 END), 0) AS Estimated_Lost_Customers,
                PRINTF("$%.2f", SUM(CASE WHEN Net_Queue_Change > 20 THEN Net_Queue_Change * 0.15 ELSE 0 END) * 9.11) AS Estimated_Lost_Revenue
            FROM tickets
            WHERE Is_Weekend = 1 AND Is_Off_Season = 0
            GROUP BY Year, Month
            ORDER BY Year DESC, Month ASC
            LIMIT 6;
        """,
        
        "2. SEASONAL CAPACITY BASELINE (STAFFING OPTIMIZATION)": """
            SELECT 
                CASE WHEN Is_Off_Season = 1 THEN 'Winter Off-Season (Nov-Apr)' 
                     ELSE 'Summer Peak-Season (May-Oct)' 
                END AS Operational_Season,
                ROUND(AVG("Sales Count"), 1) AS Avg_Sales_Per_15Min,
                ROUND(AVG("Redemption Count"), 1) AS Avg_Boardings_Per_15Min,
                MAX("Redemption Count") AS Peak_Single_15Min_Spike
            FROM tickets
            GROUP BY Is_Off_Season;
        """,
        
        "3. HOURLY SURGE PATTERNS FOR SHIFT PLANNING": """
            SELECT 
                Hour,
                CASE WHEN Is_Weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS Day_Type,
                ROUND(AVG("Redemption Count"), 1) AS Avg_Hourly_Boardings,
                MAX("Redemption Count") AS Historical_Max_Surge
            FROM tickets
            GROUP BY Hour, Is_Weekend
            ORDER BY Is_Weekend DESC, Avg_Hourly_Boardings DESC
            LIMIT 6;
        """
    }
    
    for title, sql_code in queries.items():
        print("\n" + "="*60)
        print(title)
        print("="*60)
        result_df = pd.read_sql(sql_code, conn)
        print(result_df.to_string(index=False))
        
    conn.close()
    print("\nAnalysis complete. Database connection securely closed.")

if __name__ == "__main__":
    run_business_queries()