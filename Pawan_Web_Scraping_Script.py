#We import the required modules
import requests as Pawan_Request
import lxml.html as Pawan_HTML_Reader
import pandas as Pawan_Pandas_Module

#We specify the URL Path
#url = 'C:\\Users\\brpaw\\Desktop\\Hai_Daiyya.html' -->This Does not work
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

#Create a handle, Pawan_Web_Page, to handle the contents of the website
Pawan_Web_Page = Pawan_Request.get(url)

#Store the contents of the website under Pawan_Page_Content
Pawan_Page_Content = Pawan_HTML_Reader.fromstring(Pawan_Web_Page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = Pawan_Page_Content.xpath('//tr')

#We declare all required variables
i=0
Ctr = 0
Pawan_Data_Array = []
Hisab = 0
First_Column = ''
Second_Column =''
Third_Column =''
Temp_Column =''
Temp_Column2 =''

#Hisab stores the length of all table elements in the web page (including the table we are interested in)
Hisab = len(tr_elements)

while Ctr < Hisab:
	Cell_Value = tr_elements[Ctr].text_content() #Here we obtain the vales of table elements
	if len(Cell_Value) > 0:
		First_Column = str(Cell_Value) #We obtain the value of cell in first column
		First_Column =First_Column.split("\n")[1]
		Second_Column = str(Cell_Value) #We obtain the value of cell in second column
		Second_Column = Second_Column.split("\n")[2]
		Third_Column = str(Cell_Value) #We obtain the value of cell in third column
		Third_Column = Third_Column.split("\n")[3]
		if Second_Column != 'Not assigned': #Here we eliminate the rows where second colun has 'Not Assigned' value
			if Third_Column == 'Not assigned': 
				Third_Column = Second_Column #Here we update the value of second column in third column if thitd column has 'Not Assigned' value
			elif Temp_Column == First_Column:
				Third_Column = Third_Column +', '+Temp_Column2 #Here we update third column value with previous values if first column is duplicate
				Pawan_Data_Array[i-1][0] = 'TMP'#Here we set to mark all duplicate (Unwanted)cells as TMP
			Pawan_Data_Array.append([First_Column,Second_Column,Third_Column])
			i = i+1
		Temp_Column = First_Column
		Temp_Column2 = Third_Column
		Ctr+=1
	else:
		break

#We create the dataframe		
df = Pawan_Pandas_Module.DataFrame(Pawan_Data_Array)
Header_String = df[0][0],df[1][0],df[2][0] #We create the header for the dataframe from the first row elements
df = df.iloc[1:] # We delete first row of the dataframe as it has been set as the header
df.columns = Header_String #We set the header for Data frame
df.drop_duplicates('Postcode',keep = False, inplace = True) #Here we eliminate duplicate rows
print(df)
