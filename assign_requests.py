import mysql.connector
import datetime
import script
import random

mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )


cursor = mydatabase.cursor()

#Παίρνω όλες τις τιμές, ταξιμομημένες  απο την μεγαλύτερη στην μικρότερη μετρική total_rate 
sql = "SELECT * FROM metrics ORDER BY total_rate DESC"
cursor.execute(sql)
metrics_results = cursor.fetchall()

distributors = [row[0] for row in metrics_results]
total = [row[2] for row in metrics_results]
shift = [row[1] for row in metrics_results]   #για την μερα που πηρα την μετρική 
#ταξιμομημένοι σωστά
print(distributors)
print(total)



 # Παiρνω ολα τα αιτήματα ταξιμομημένα απο το μικρότερη προς την μεγαλυτερη απόσταση μεταξύ των locations
sql_aitima = "SELECT * FROM Aitima ORDER BY expected_difference_km"
cursor.execute(sql_aitima)
aitimata = [row[0] for row in cursor.fetchall()]     #ta3inomimena aitimata
mydatabase.commit()
 
print(aitimata)       

today = datetime.datetime.today().strftime('%Y-%m-%d')
yesterday =  datetime.date.today().strftime('%Y-%m-%d') #το βαζω μονο για σημερα για να το τεστάρω 
#yesterday =  datetime.date.today() datetime.timedelta(days=1)
print(yesterday) #χθεσινη μερα 
print(today)


if today == yesterday:
    print("Aitima is updated.")
    # Delete the assigned distributors and times for all requests
    cursor = mydatabase.cursor()
    cursor.execute("UPDATE Aitima SET id_distr = NULL, time_aitimatos = NULL, date_aitimatos = NULL")
    mydatabase.commit()
    
      
if(today==yesterday):
      
        cursor = mydatabase.cursor()
        cursor.execute("DELETE  FROM Shift")
        mydatabase.commit()
        print("Shift is Null.")
#ασ μην κανω ακομα delete τα δεδομενα για τους πινακες metrics, metrics_store, metrics_costumer, metrics_comapny 
        
if(today==yesterday):
        
        cursor = mydatabase.cursor()
        cursor.execute("DELETE  FROM RatingFromBroker")
        mydatabase.commit()
        print("RatingFromCompany is Null.")

if(today==yesterday):
        
        cursor = mydatabase.cursor()
        cursor.execute("DELETE  FROM RatingFromStore")
        mydatabase.commit()
        print("RatingFromStore is Null.")
      
if(today==yesterday):
       
        cursor = mydatabase.cursor()
        cursor.execute("DELETE  FROM RatingFromCostumer")
        mydatabase.commit()
        print("RatingFromStore is Null.")


if(today==yesterday):
        #δηλώνω ραντομ Shift για διανομείς
  #  script.Dilwsi_Shift()

        #Aνάθεση αιτημάτων με βάση τις μετρικές αντί για ραντομ 
        #δίνω στον διανομέα με την μεαλύτερη μετρική (έστω την συνολική) το πιο κοντινό αίτημα και περισσότερα αιτήματα

    mydatabase = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="123456789",
                        database="diplomatiki11"
                )

    cursor = mydatabase.cursor()


                        #αναθέτω τα 5 πρωτα αιτήματα στον διανομεα με την καλύτερη μετρική 

                        #βαζω καμια ώρα ραντομ μέσα στα πλάισια του νέου shift 
                        

#παίρνω τον διανομέα με το καλύτερο total_rate (distributors[0])


        
#Για τον διανομέα με την καλύτερη μετρική  δωστου τα 5 πιο κοντινα αιτήματα 

Aitimata = aitimata[:5]
print(distributors[0])



# Print the first 5 aitimata assigned to distributors[0]
print(Aitimata[0])


# Get the first 5 aitimata and assign them to the first element of the distributors list
Aitimata[0] = aitimata[:5]

# Loop over the first 5 aitimata and update the table with a random time for each aitima
for aitima_id in Aitimata[0]:
    # Get the time starts and time ends for the distributor
    sql = "SELECT time_starts, time_ends FROM Shift WHERE ID_distributor_shift = %s"
    params = (distributors[0],)
    cursor.execute(sql, params)
    shift_times = cursor.fetchone()

    # Generate a random time within the shift times
    time_starts = shift_times[0]
    time_ends = shift_times[1]
    random_time = random.uniform(time_starts, time_ends)

    # Update the Aitima table with the random time for the current aitima
    sql = "UPDATE Aitima SET id_distr= %s, date_aitimatos=%s, time_aitimatos=%s WHERE id_aitimatos= %s"
    params = (distributors[0],today,random_time, aitima_id)
    cursor.execute(sql, params)

# Commit the changes to the database
mydatabase.commit()


#Για τον διανομεα distributor[1] δωστου τα 4 πιο κοντινα επομενα αιτήματα 
Aitimata1 = aitimata[5:9]
print(Aitimata1)

print(distributors[1])

# Loop over the first 5 aitimata and update the table with a random time for each aitima
for aitima_id in Aitimata1:
    # Get the time starts and time ends for the distributor
    sql = "SELECT time_starts, time_ends FROM Shift WHERE ID_distributor_shift = %s"
    params = (distributors[1],)
    cursor.execute(sql, params)
    shift_times = cursor.fetchone()

    # Generate a random time within the shift times
    time_starts = shift_times[0]
    time_ends = shift_times[1]
    random_time = random.uniform(time_starts, time_ends)

    # Update the Aitima table with the random time for the current aitima
    sql = "UPDATE Aitima SET id_distr= %s, date_aitimatos=%s, time_aitimatos=%s WHERE id_aitimatos = %s"
    params = (distributors[1],today,random_time, aitima_id)
    cursor.execute(sql, params)

# Commit the changes to the database
mydatabase.commit()
"""

"""
#Για τον διανομεα distributors[2] τα επόμενα 3 
Aitimata2 = aitimata[9:12]


# Loop over the first 5 aitimata and update the table with a random time for each aitima
for aitima_id in Aitimata2:
    # Get the time starts and time ends for the distributor
    sql = "SELECT time_starts, time_ends FROM Shift WHERE ID_distributor_shift = %s"
    params = (distributors[2],)
    cursor.execute(sql, params)
    shift_times = cursor.fetchone()

    # Generate a random time within the shift times
    time_starts = shift_times[0]
    time_ends = shift_times[1]
    random_time = random.uniform(time_starts, time_ends)

    # Update the Aitima table with the random time for the current aitima
    sql = "UPDATE Aitima SET id_distr= %s, date_aitimatos=%s, time_aitimatos=%s WHERE id_aitimatos = %s"
    params = (distributors[2],today,random_time, aitima_id)
    cursor.execute(sql, params)

# Commit the changes to the database
mydatabase.commit()


#Για τον διανομέα distributor[3] to get the next 2 requests
Aitimata3 = aitimata[12:14]


# Loop over the first 2 aitimata and update the table with a random time for each aitima
for aitima_id in Aitimata3:
    # Get the time starts and time ends for the distributor
    sql = "SELECT time_starts, time_ends FROM Shift WHERE ID_distributor_shift = %s"
    params = (distributors[3],)
    cursor.execute(sql, params)
    shift_times = cursor.fetchone()

    # Generate a random time within the shift times
    time_starts = shift_times[0]
    time_ends = shift_times[1]
    random_time = random.uniform(time_starts, time_ends)

    # Update the Aitima table with the random time for the current aitima
    sql = "UPDATE Aitima SET id_distr= %s, date_aitimatos=%s, time_aitimatos=%s WHERE id_aitimatos = %s"
    params = (distributors[3],today,random_time, aitima_id)
    cursor.execute(sql, params)

# Commit the changes to the database
mydatabase.commit()

#Για ολους τους υπολοιπους διανομείς να παίρνουν από 1. 

num_distributors = 6  # Ποσοι distributors μένουν για να δώσω αιτήματα 
start_index = 14  # απο ποιο αίτημα θα ξεκινήσει να αναθέτει

for i in range(num_distributors):
    distributor_index = i + 4  
    aitima_index = start_index + i  
    Aitimata = [aitimata[aitima_index]]  
    
     # Get the time starts and time ends for the distributor
    sql = "SELECT time_starts, time_ends FROM Shift WHERE ID_distributor_shift = %s"
    params = (distributors[distributor_index],)
    cursor.execute(sql, params)
    shift_times = cursor.fetchone()

    # Generate a random time within the shift times
    time_starts = shift_times[0]
    time_ends = shift_times[1]
    random_time = random.uniform(time_starts, time_ends)

    # Update the Aitima table with the random time for the current aitima
    sql = "UPDATE Aitima SET id_distr= %s, date_aitimatos=%s, time_aitimatos=%s WHERE ID_aitimatos = %s"
    params = (distributors[distributor_index],today,random_time, aitimata[aitima_index])
    cursor.execute(sql, params)

#μετα σβήνω και τους μετριψσ και τους total rate 

if today == yesterday:
    print("Aitima is updated.")
    