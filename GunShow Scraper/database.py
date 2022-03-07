import mysql.connector

#mydb = mysql.connector.connect(
#  host="db4free.net",
#  user="gunshowdb",
#  password="31175209",
# database="gunshow"
#)



mydb = mysql.connector.connect(
  host="34.72.135.103",
  user="senmfxghwx",
  password="wHTVqb7Sx2",
  database="senmfxghwx", 
  port = '22'
)


mycursor = mydb.cursor()
mycursor.execute('SELECT table_name FROM information_schema.tables;')

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

'''

mycursor.execute("DROP TABLE IF EXISTS `dates`;")

mycursor.execute("DROP TABLE IF EXISTS `gun_shows`;")
mycursor.execute("DROP TABLE IF EXISTS `promoters`;")

mycursor.execute("CREATE TABLE `dates`  (`id` int(11) NOT NULL AUTO_INCREMENT,`gun_show_id` int(11) NULL DEFAULT NULL,`promoter_id` int(11) NULL DEFAULT NULL,`start_date` datetime(0) NOT NULL,`end_date` datetime(0) NULL DEFAULT NULL,`cancelled` tinyint(1) NULL DEFAULT NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;")






mycursor.execute("""CREATE TABLE `promoters`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `logo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `name` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `contact` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  UNIQUE(name),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;""")




mycursor.execute("""CREATE TABLE `gun_shows`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `promoter_id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `state` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `hours` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `admission` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `venue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `venue_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `venue_city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `venue_state` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `venue_zip` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `vendor_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_date` datetime(0) NOT NULL,
  `updated_date` datetime(0) NULL DEFAULT NULL,
  UNIQUE(name),
  FOREIGN KEY(promoter_id) REFERENCES promoters(id),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;""")








mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")



'''
