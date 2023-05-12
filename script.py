
import mysql.connector
import datetime
from geopy.distance import geodesic
import random
import osmium
import requests
import os
import json
import osmnx.distance as distance
import osmnx as ox
import networkx as nx
from random import uniform
import pandas as pd
import cgi


#Inser a Distributor to the Database


def InsertDistributor_toDatabase():
    
    #dinw timi apo ton terminal 
    value1= input("Enter the username of the distributor:")
    value2=input("Enter the password of the distributor:")
    
    #kanw connection tou python file mou me tin mydatabase
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )
     
    # ftiaxnw ton cursorako pou allilepidra me database
    cursor = mydatabase.cursor()
     
    #edw pairnei thn timi apo ton terminal kai tin bazei stin basi
    sql = "INSERT INTO Distributor (username_distributor,password_distributor) VALUES (%s,%s)"
    val = (value1,value2)
    
    # execute the SQL 
    cursor.execute(sql, val)
    
    #kanw panta ena commit 
    mydatabase.commit()

    # close the cursor and database connection
    cursor.close()
    mydatabase.close()

    print("Distributor added to the database!")




def Kataxwrise_Aitima_database():
   
    

    # kanw connection tou python file mou me tin mydatabase
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )

    # ftiaxnw ton cursorako pou allilepidra me database
    cursor = mydatabase.cursor()
    
            
    #BHMA1: Bazw estw thn Patra kai pairnw ta data gia to odiko ths diktio 
    city = "Patras, Greece"
    graph = ox.graph_from_place(city, network_type="drive")
            
    
    store_node, customer_node = random.sample(list(graph.nodes()), k=2)
            
            #ΒΗΜΑ3: Παίρνω lon και lat για καθεμία απο τις 2 τοποθεσίες από το οδικό δίκτυο
    store_coords = graph.nodes[store_node]["x"], graph.nodes[store_node]["y"]
    customer_coords = graph.nodes[customer_node]["x"], graph.nodes[customer_node]["y"]
            
            #ΒΗΜΑ4: Βρίσκω την απόσταση μεταξύ τους (ελάχιστη, /1000 γιατι το θελω σε χιλιόμετρα)
    distance = float(round(nx.shortest_path_length(graph, store_node, customer_node, weight='length')/1000, 2)) # numpy.float64 to float
            #Έλεγχος να εμφανίζεται στον τέρμιναλ αν βρήκα τέλος πάντων δρόμο και συντεταγμένες για τις τοποθεσίες ΠΡΙΝ ΤΑ ΕΙΣΑΓΩ ΣΤΗΝ ΒΆΣΗ 
            #H print εκτυπώνει τιμές άρα πάει καλα!!!!!!! 
    print(f"store: {store_coords}, customer: {customer_coords}, distance: {distance}")
            
            
            #INSERT EPITELOUSSSS!!!!!!!!!
            
    sql = "INSERT INTO Aitima (latitude_store, longitude_store, latitude_costomer, longtitude_costumer, expected_difference_km) VALUES (%s, %s, %s, %s,  CAST(%s AS DECIMAL(10,2)))"
    val = ( store_coords[0], store_coords[1], customer_coords[0], customer_coords[1], distance)

    print(cursor.rowcount, "Request added to the database!")   
            # execute the SQL 
    cursor.execute(sql, val)
    mydatabase.commit()
    

def Dilwsi_Shift():
    # sundesi me basi
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )

    # cursorakos
    cursor = mydatabase.cursor()

    #yparxei autos o dianomeas stin basi?
    sql = "SELECT id_distributor FROM Distributor"
    cursor.execute(sql)
    distributor_ids = cursor.fetchall()

    # input imerominia
    Hmerominia = datetime.datetime.today().strftime('%Y-%m-%d')

    # elegxos an i hmerominia einai valid! px den thelw na balw to 1821 ws mera bardias.
    try:
        Hmerominia = datetime.datetime.strptime(Hmerominia, '%Y-%m-%d')
        if Hmerominia.year < datetime.datetime.now().year: #mono gia to etos 2021 kai panw ton afinw
            print("Invalid year entered.")
        elif Hmerominia.month < 1 or Hmerominia.month > 12: #profanws ama baleis mina 13 d
            print("Invalid month entered.")
        elif Hmerominia.day < 1 or Hmerominia.day > 31: # 38 tou mina
            print("Invalid day entered.")
        else:
            print("Date entered is valid.")
    except ValueError:
        print("Invalid date format entered.")

    # gia kathe distributor, dimiourgo random ora enarxis kai lixis kai kanw insert stin database
    for distributor_id in distributor_ids:
        distributor_id = distributor_id[0]
        wra_enarxis_shift = datetime.time(hour=random.randint(8, 12), minute=random.randint(0, 59), second=random.randint(0, 59))
        wra_lixis_shift = datetime.time(hour=random.randint(13, 20), minute=random.randint(0, 59), second=random.randint(0, 59))

        # afou einai swsta, pame na ta kanoume insert stin database
        sql = "INSERT INTO Shift (date_shift, ID_distributor_shift, time_starts, time_ends) VALUES (%s, %s, %s, %s)"
        val = (Hmerominia, distributor_id, wra_enarxis_shift, wra_lixis_shift)

        # Execute
        cursor.execute(sql, val)
        mydatabase.commit()

        # Gia na eimai sigouri oti egine h eggrafi stin basi
        print(cursor.rowcount, "record inserted for distributor id", distributor_id)

    print("Shifts declared for all distributors on", Hmerominia)




def Apodoxi_Aitimatos_Distributor():
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )

    cursor = mydatabase.cursor()

    # παίρνω την σημερινή ημερομηνία
    date_input = datetime.date.today().strftime("%Y-%m-%d")

    # Παίρνω τους διανομείς που έχουν βάρδια αυτή την μέρα 
    sql_shift = "SELECT ID_distributor_shift FROM Shift WHERE date_shift = %s"
    val_shift = (date_input,)
    cursor.execute(sql_shift, val_shift)
    distributors = [row[0] for row in cursor.fetchall()]

    if not distributors:
        print("No distributors have a shift today.")
        return

    # Αναθέτω στους διανομείς ΤΥΧΑΙΑ όλα τα αιτήματα από τον πίνακα Aitima
    sql_aitima = "SELECT id_aitimatos FROM Aitima"
    cursor.execute(sql_aitima)
    aitimata = [row[0] for row in cursor.fetchall()]
    #αρχικοποιηση για να βρω το acceptance_rate κάθε distributor 
    distributor_stats = {d: {"total_requests": 0, "accepted_requests": 0} for d in distributors}

    for aitima in aitimata:
        
        while True:
            #επιλέγω random distributor απ΄αυτους που έχω πάρει απο την βάση
            random_distributor = random.choice(distributors)
            #μετρα τα συνολικά αιτηματα, πρεπει να βρισκεται εδω;;;;;
            distributor_stats[random_distributor]["total_requests"] += 1

            # παίρνω την βάρδια του διανομεα του τυχαίου για την σημερινή μέρα 
            sql_shift = "SELECT time_starts, time_ends FROM Shift WHERE date_shift = %s AND ID_distributor_shift = %s"
            val_shift = (date_input, random_distributor)
            cursor.execute(sql_shift, val_shift)
            shift_result = cursor.fetchone()

            if shift_result is None:
                print(f"Invalid distributor {random_distributor} or date {date_input}.")
                return
            #ωρες εναρξης και ληξης 
            shift_start = datetime.datetime.strptime(str(shift_result[0]), "%H:%M:%S")
            shift_end = datetime.datetime.strptime(str(shift_result[1]), "%H:%M:%S")

            # τυχαία αποφασίζω αν θα αναλάβει ή θα απορρίψει το αίτημα (ίσως θα πρέπει να μην ειναι ραντομ και να πηγαινει με βαση τα expected km των αιτημάτων)
            value = random.randint(0, 1)
            
            if value == 1:
                # Αν ο διανομέας αποδεχτεί το αίτημα, βάλε μια τυχαια time_aitimatos προφανώς μέσα στην ώρα που έχει βάρδια ο διανομέας
                random_time = datetime.datetime.combine(datetime.date.today(), shift_start.time()) + datetime.timedelta(
                    seconds=random.randint(0, int((shift_end - shift_start).total_seconds()))
                )
                time_aitimatos = random_time.strftime("%H:%M:%S")
                distributor_stats[random_distributor]["accepted_requests"] += 1 #δεν δουλευει
                if random_time.time() >= shift_start.time() and random_time.time() <= shift_end.time():
                    time_aitimatos = random_time.strftime("%H:%M:%S")
                else:
                    continue
                
                # Update the Aitima table with acceptance status and time
                sql_update = "UPDATE Aitima SET id_distr=%s ,time_aitimatos = %s, date_aitimatos = %s, accepted=1 WHERE id_aitimatos = %s"
                val_update = (random_distributor, time_aitimatos, date_input, aitima)
                cursor.execute(sql_update, val_update)
                mydatabase.commit()
                
                
                
                break
            else:
                
                
                #Αν απορρίφθηκε => σε αλλον διανομέα,οχι στον ιδιο 
                remaining_distributors = [d for d in distributors if d != random_distributor]
                if not remaining_distributors:
                    print(f"All distributors have declined request {aitima}.")
                    break
                #κανε την ιδια διαδικασία
                random_distributor = random.choice(remaining_distributors)

    #δεν δουλευει το acceptance_rate
    
    """
    cursor = mydatabase.cursor()
    for distributor in distributor_stats:
        acceptance_rate = distributor_stats[distributor]["accepted_requests"] / distributor_stats[distributor]["total_requests"]
        sql_update = "UPDATE Shift SET acceptance_rate = %s, Total_aitimata_per_shift=%s WHERE ID_distributor_shift = %s AND date_shift = %s"
        val_update = (acceptance_rate, distributor_stats[distributor]["accepted_requests"],distributor, date_input)
        cursor.execute(sql_update, val_update)
        mydatabase.commit()
    """
    cursor.close()
    mydatabase.close()



def Rating_From_Store():
    # Connect to database
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )
    
    # Get current date
    
    current_date =datetime.date.today().strftime("%Y-%m-%d")
    
    # Select requests with current date
    cursor = mydatabase.cursor()
    sql1 = "SELECT id_aitimatos FROM Aitima WHERE date_aitimatos = %s"
    val1 = (current_date,)
    cursor.execute(sql1, val1)
    result1 = cursor.fetchall()
    
    if len(result1) == 0:
        print("No requests with current date found!")
    else:
        for request in result1:
            # Select distributor for request
            cursor = mydatabase.cursor()
            sql2 = "SELECT id_distributor FROM Distributor WHERE id_distributor IN (SELECT id_distr FROM Aitima WHERE id_aitimatos = %s)"
            val2 = (request[0],)
            cursor.execute(sql2, val2)
            result2 = cursor.fetchall()
            
            if len(result2) == 0:
                print("No distributor found for request with id:", request[0])
            else:
                # Choose random rating for distributor and request
                rating1 = str(random.randint(1, 5)) # random integer between 1 and 5
                rating2 = str(random.randint(1, 5)) # random integer between 1 and 5
                rating3 = str(random.randint(1, 5)) # random integer between 1 and 5
                distributor_id = result2[0][0]
                
                # Check if rating already exists
                cursor = mydatabase.cursor()
                sql3 = "SELECT * FROM RatingFromStore WHERE id_di=%s AND dat_shift=%s AND id_aitim=%s"
                val3 = (distributor_id, current_date, request[0])
                cursor.execute(sql3, val3)
                result3 = cursor.fetchall()

                if len(result3) > 0:
                    print("A rating for distributor with id:", distributor_id, "and request with id:", request[0], "already exists.")
                else:
                    # Insert rating into table
                    cursor = mydatabase.cursor()
                    sql4 = "INSERT INTO RatingFromStore (id_di, dat_shift, id_aitim, speed,accuracy,customer_service) VALUES (%s, %s, %s, %s,%s,%s)"
                    val4 = (distributor_id, current_date, request[0], rating1,rating2,rating3)

                    try:
                        cursor.execute(sql4, val4)
                        mydatabase.commit()
                        print("Rating of", rating1,rating2,rating3 ,"inserted for distributor with id:", distributor_id, "and request with id:", request[0])
                    except mysql.connector.Error as error:
                        print("Failed to insert record into RatingFromStore table {}".format(error))
        
    # Close database connection
    mydatabase.close()
    

        
def Actual_km():
        
    #pros to paron mias kai den exw gps akoma. apla gia testing 
        
        
    # kanw connection tou python file mou me tin mydatabase
    mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
    cursor = mydatabase.cursor()
    id_paraggelias=input("Give me the id of the order:")
    #elegxw an paraggelia me auto to id kai an einai accepted. An kapoio apo ta dio den isxeiei den proxwraw
    sql = "SELECT id_aitimatos FROM Aitima WHERE id_aitimatos = %s AND accepted=1" 
    val = (id_paraggelias,)
    
    cursor.execute(sql, val)
    result = cursor.fetchone()   
    
    #αν αυτο που παρω ειναι τιποτα βγαλε ενα απλα print που ενημερωνει για μη εγκυρα στοιχεια 
    #αν παρω βαλε κανε ινσερτ στον πινακα, αφου πρωτα ζητησεις τα actual km 
    if result is None:
        print(f"The order does not exist or its not accepted from distributor!")
    else: 
         #zhta timoula 
         
         pragmatika_km=input("Give me the actual km the distributor for the delivery: ")
         
         sql2 = "UPDATE Aitima SET real_klm = %s WHERE id_aitimatos = %s"
         val2 = (pragmatika_km, id_paraggelias)
         cursor.execute(sql2, val2)
         mydatabase.commit()


def Rating_From_Broker():
    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Connect to database
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )
    cursor = mydatabase.cursor()

    # Get all requests with the current date
    sql1 = "SELECT id_aitimatos FROM Aitima WHERE date_aitimatos=%s"
    val1 = (current_date,)
    cursor.execute(sql1, val1)
    requests = cursor.fetchall()

    # Generate and store ratings for each request
    for request in requests:
        # Get distributor ID for request
        sql2 = "SELECT id_distr FROM Aitima WHERE id_aitimatos=%s"
        val2 = (request[0],)
        cursor.execute(sql2, val2)
        distributor_id = cursor.fetchone()[0]

        # Generate random rating
        rating1 = random.randint(1, 5)
        rating2 = random.randint(1, 5)
        rating3 = random.randint(1, 5)
        # Check if rating already exists
        sql3 = "SELECT * FROM RatingFromBroker WHERE id_di=%s AND dat_shift=%s AND id_aitim=%s"
        val3 = (distributor_id, current_date, request[0])
        cursor.execute(sql3, val3)
        result3 = cursor.fetchall()

        if len(result3) > 0:
            print(f"A rating for distributor ID {distributor_id}, delivery date {current_date}, and order ID {request[0]} already exists.")
        else:
            # Insert rating into database
            sql4 = "INSERT INTO RatingFromBroker (id_di, dat_shift, id_aitim, speed,accuracy,customer_service) VALUES (%s, %s, %s, %s, %s, %s)"
            val4 = (distributor_id, current_date, request[0], rating1,rating2,rating3)

            try:
                cursor.execute(sql4, val4)
                mydatabase.commit()
                print(f"Rating of {rating1,rating2,rating3} for distributor ID {distributor_id}, delivery date {current_date}, and order ID {request[0]} has been stored.")
            except mysql.connector.Error as error:
                print(f"Failed to insert record into RatingFromBroker table: {error}")

    # Close database connection
    cursor.close()
    mydatabase.close()


def Rating_From_Costumer():

    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )

    cursor = mydatabase.cursor()

    # Get all requests from Aitima table with the current date
    sql1 = "SELECT id_aitimatos, id_distr FROM Aitima WHERE date_aitimatos = %s"
    val1 = (current_date,)
    cursor.execute(sql1, val1)
    results1 = cursor.fetchall()

    if len(results1) == 0:
        print("No requests found for the current date!")
        return
    
    # Iterate over each request and rate the distributor
    for result1 in results1:
        value1 = result1[1]
        value2 = current_date
        value3 = result1[0]
        value4 = random.randint(1, 5)
        value5 = random.randint(1, 5)
        value6 = random.randint(1, 5)

        # Check if distributor exists
        sql2 = "SELECT id_distributor FROM Distributor WHERE id_distributor = %s"
        val2 = (value1,)
        cursor.execute(sql2, val2)
        result2 = cursor.fetchall()

        if len(result2) == 0:
            print("No distributor found with the given ID: ", value1)
        else:
            # Check if rating already exists for this request and distributor
            sql3 = "SELECT id_rating_costumer FROM RatingFromCostumer WHERE id_aitimatos_costumer = %s AND id_rating_costumer = %s"
            val3 = (value3, value1)
            cursor.execute(sql3, val3)
            result3 = cursor.fetchall()

            if len(result3) != 0:
                print("Rating already exists for this request and distributor!")
            else:
                # Insert rating into RatingFromCostumer table
                cursor = mydatabase.cursor()
                sql4 = "INSERT INTO RatingFromCostumer (dat_shif_costumer, id_aitimatos_costumer, id_rating_costumer , speed, accuracy, customer_service) VALUES (%s, %s, %s, %s, %s, %s)"
                val4 = (value2, value3, value1, value4, value5, value6)

                try:
                    cursor.execute(sql4, val4)
                    mydatabase.commit()
                    print("Rating added successfully for distributor ID:", value1)
                except mysql.connector.Error as error:
                    print("Failed to insert record into RatingFromCostumer table: ", error)

    cursor.close()
    mydatabase.close()



def metrics():

    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )

    cursor = mydatabase.cursor()

    # παιρνω ολους τους διανομεις απο το Shift 
    cursor.execute("SELECT DISTINCT ID_distributor_shift FROM Shift")
    distributor_ids = cursor.fetchall()

    # loop για να το κανω για καθε διανομεα 
    for distributor_id in distributor_ids:
        distributor_id = distributor_id[0]  # παιρνω την τιμη του διανομεα απο το tuple 

        # Για τον συγκεκριμενο διανομεα παρε ολα τα Shifts 
        query = "SELECT * FROM Shift WHERE ID_distributor_shift = %s"
        cursor.execute(query, (distributor_id,))
        shifts = cursor.fetchall()

        # Για καθε βαρδια βρίσκω την συνέπεια στην εναρξη και την ληξη 
        for shift in shifts:
            shift_start_time = shift[7]
            shift_end_time = shift[8]
            shift_date = shift[0]

            query = "SELECT time_aitimatos FROM Aitima WHERE id_distr = %s AND date_aitimatos = %s AND accepted=1 ORDER BY time_aitimatos ASC LIMIT 1"
            cursor.execute(query, (distributor_id, shift_date))

            result = cursor.fetchone()
            if result is not None:
                first_request_time = result[0]
            else:
                first_request_time = shift_start_time  # Assign default value
                print("No data to retrieve for first request time")

            query = "SELECT time_aitimatos FROM Aitima WHERE id_distr = %s AND date_aitimatos = %s AND accepted=1 ORDER BY time_aitimatos DESC LIMIT 1"
            cursor.execute(query, (distributor_id, shift_date))

            result1 = cursor.fetchone()
            if result1 is not None:
                last_request_time = result1[0]
            else:
                last_request_time = shift_end_time  # Assign default value
                print("No data to retrieve for last request time")

            time_diff_to_first_request = (first_request_time - shift_start_time).total_seconds()
            time_diff_to_last_request = (shift_end_time - last_request_time).total_seconds()

            # Απλα και μονο για να δω αν δουλευει, (δουλευει)
            print(f"Shift on {shift_date}:")
            print(f"Time difference to first request accepted: {time_diff_to_first_request} seconds")
            print(f"Time difference to last request accepted: {time_diff_to_last_request} seconds")

           
           
            # Απλα και μονο για να δω αν δουλευει, (δουλευει)
            print(f"Shift on {shift_date}:")
            print(f"Time difference to first request accepted: {time_diff_to_first_request} seconds")
            print(f"Time difference to last request accepted: {time_diff_to_last_request} seconds")
            
        
             # insert the calculated values into the metrics table
            cursor.execute("INSERT INTO metrics ( distributor_id, shift, sunepeia_enarxi, sunepeia_lixi) VALUES (%s, %s, %s,%s)",
                (distributor_id, shift_date, time_diff_to_first_request, time_diff_to_last_request))
        
        # μο ανα εκτιμώμενων χλμ / accepted αιτήματα
       
            query = """
                SELECT 
                    s.date_shift, 
                    s.ID_distributor_shift,
                    s.Total_aitimata_per_shift,
                    SUM(a.expected_difference_km) / SUM(a.accepted) AS avg_distance_per_accepted_request
                FROM 
                    Shift s 
                    JOIN Aitima a ON s.ID_distributor_shift = a.id_distr AND s.date_shift = a.date_aitimatos
                WHERE 
                    s.ID_distributor_shift = %s AND a.accepted = 1
                GROUP BY 
                    s.date_shift, 
                    s.ID_distributor_shift
                """

            cursor.execute(query, (distributor_id,))
            results = cursor.fetchall()

            # Print the results for this distributor
            print(f"For distributor {distributor_id}:")
            for row1 in results:
                print(f"Date: {row1[0]}, Avg. distance per accepted request: {row1[3]}")
                update_metrics_query="UPDATE metrics SET accepted_requests=%s, average_distance_k=%s WHERE distributor_id=%s AND shift=%s "
                values_updated=(row1[2],row1[3],distributor_id,row1[0])
                cursor.execute(update_metrics_query, values_updated)
                

            # overhead calculation
            query = """
                SELECT 
                    s.date_shift, 
                    s.ID_distributor_shift, 
                    SUM(a.real_klm) / SUM(a.expected_difference_km) AS overhead
                FROM 
                    Shift s 
                    JOIN Aitima a ON s.ID_distributor_shift = a.id_distr AND s.date_shift = a.date_aitimatos
                WHERE 
                    s.ID_distributor_shift = %s AND accepted=1
                GROUP BY 
                    s.date_shift, 
                    s.ID_distributor_shift
                """

            cursor.execute(query, (distributor_id,))
            results = cursor.fetchall()

            # Print the results for this distributor
            print(f"For distributor {distributor_id}:")
            for row in results:
                print(f"Date: {row[0]}, Overhead: {row[2]}")
                update_metrics_query="UPDATE metrics SET overhead_real=%s WHERE distributor_id=%s AND shift=%s "
                values_updated=(row[2],row[1],row[0])
                cursor.execute(update_metrics_query, values_updated)
                

        
            #pame na kanoume  to rating ton dianomewn apo to katastima kai na ta baloume ston metrics ! 
            
            
                    
    
        #gia na mpoun oi times sto metrics_costumer                   
            query_rating_costumer1 = """
                SELECT 
                    r.dat_shif_costumer, 
                    r.id_rating_costumer, 
                    AVG(r.speed) as speed,
                    AVG(r.accuracy) as accuracy,
                    AVG(r.customer_service) as customer_service
                    
                    
                FROM 
                    RatingFromCostumer r 
                    JOIN Aitima a ON r.id_rating_costumer = a.id_distr AND  r.dat_shif_costumer= a.date_aitimatos AND r.id_aitimatos_costumer= a.id_aitimatos
                WHERE 
                    r.id_rating_costumer = %s 
                GROUP BY 
                    r.dat_shif_costumer, 
                    r.id_rating_costumer
                """
           
            cursor.execute(query_rating_costumer1, (distributor_id,))
            results_rating_costumer1 = cursor.fetchall()
           
            
            for row5 in results_rating_costumer1:        
              cursor.execute("INSERT IGNORE INTO metrics_costumer (speed, accuracy,customer_service , distributor_id, shift) VALUES (%s, %s, %s, %s, %s)",
               (row5[2], row5[3], row5[4], row5[1], row5[0]))
              
            query_rating_store1 = """
                    SELECT 
                        r.dat_shift, 
                        r.id_di, 
                        r.id_aitim,
                        AVG(r.speed) as speed,
                        AVG(r.accuracy) as accuracy,
                        AVG(r.customer_service) as customer_service
                        
                    FROM 
                        RatingFromStore r 
                        JOIN Aitima a ON r.id_di = a.id_distr AND  r.dat_shift= a.date_aitimatos AND r.id_aitim= a.id_aitimatos
                    WHERE 
                        r.id_di = %s 
                    GROUP BY 
                        r.dat_shift, 
                        r.id_di
                    """
            
            cursor.execute(query_rating_store1, (distributor_id,))
            results_rating_store1 = cursor.fetchall()
         

            
            for row12 in results_rating_store1:        
                cursor.execute("INSERT IGNORE  INTO metrics_store ( speed,accuracy,customer_service,distributor_id, shift ) VALUES (%s,%s,%s,%s,%s)",
                 (row12[3],row12[4],row12[5],row12[1],row12[0]))
                            
            query_rating_broker = """
                    SELECT 
                        r.dat_shift, 
                        r.id_di, 
                        r.id_aitim,
                    AVG( r.speed) as speed,
                    AVG( r.accuracy) as accuracy,
                    AVG( r.customer_service) as customer_service
                        
                    FROM 
                        RatingFromBroker r 
                        JOIN Aitima a ON r.id_di = a.id_distr AND  r.dat_shift= a.date_aitimatos AND r.id_aitim= a.id_aitimatos
                    WHERE 
                        r.id_di = %s 
                    GROUP BY 
                        r.dat_shift, 
                        r.id_di
                    """
            
            cursor.execute(query_rating_broker, (distributor_id,))
            results_rating_broker = cursor.fetchall()
            
           

            for row12 in results_rating_broker:        
                cursor.execute("INSERT IGNORE INTO metrics_broker ( speed,accuracy,customer_service,distributor_id, shift) VALUES (%s,%s,%s,%s,%s)   ",
                 (row12[3],row12[4],row12[5],row12[1],row12[0]))
            
            
    mydatabase.commit()
    cursor.close()
    mydatabase.close()
   
def assing_requests_total_rate():
    
    #Aνάθεση αιτημάτων με βάση τις μετρικές αντί για ραντομ 
        #δίνω στον διανομέα με την μεαλύτερη μετρική (έστω την συνολική) το πιο κοντινό αίτημα και περισσότερα αιτήματα

    mydatabase = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="123456789",
                        database="diplomatiki11"
    )

    
    cursor = mydatabase.cursor()

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    yesterday =  datetime.date.today() - datetime.timedelta(days=1)
    
    # Get all requests sorted by expected_difference_km from smallest to largest
    cursor.execute("SELECT id_aitimatos, id_distr, expected_difference_km FROM Aitima ORDER BY expected_difference_km")
    requests = cursor.fetchall()
    mydatabase.commit()

    # Get all distributors who have a shift today
    cursor.execute("SELECT ID_distributor_shift FROM Shift WHERE date_shift = %s", (today,))
    distributors = [row[0] for row in cursor.fetchall()]
    mydatabase.commit()

    # For each distributor on shift, get their total_rate from yesterday's metrics
    # Sort the distributors by total_rate in descending order
    sort_distributors_onshift = []
    for distributor in distributors:
        cursor.execute("SELECT total_rate, total_customer_service FROM metrics WHERE distributor_id = %s AND shift = %s", (distributor, yesterday))
        total_rate, total_customer_service = cursor.fetchone()
        sort_distributors_onshift.append((distributor, total_rate, total_customer_service))
    mydatabase.commit()
    sort_distributors_onshift.sort(key=lambda x: (-x[1], -x[2]))  # Sort by total_rate in descending order, then by total_customer_service in descending order
    
    # Assign each request to the distributor with the highest total_rate until all distributors on shift have one request
    for distributor_info in sort_distributors_onshift:
        distributor = distributor_info[0]
        for request in requests:
            
            if request[1] == None:  # Check if request hasn't been assigned yet
                cursor.execute("UPDATE Aitima SET id_distr = %s, time_aitimatos = %s, date_aitimatos = %s, accepted = %s WHERE id_aitimatos = %s", (distributor, datetime.datetime.now().strftime('%H:%M:%S'), today, 1, request[0]))
                mydatabase.commit()
                request[1] = distributor  # Mark request as assigned
                break  # Move to next distributor
            
    # Get all unassigned requests
    unassigned_requests = [request for request in requests if request[1] == None]
    remaining_requests = len(unassigned_requests)
    
    
    
    mydatabase.close()
    
    return remaining_requests
        