###############################################################################
#Generates the boxes for the advising page with the correct colors and correct values for the buttons
def getButton(student_name, className, grade, comment):
    if grade == '':
        gradeFormat = "None"
    else:
        gradeFormat = grade
    
    if comment == None:
        commentFormat = "None"
    else:
        commentFormat = comment
        
    fail = ['D+' 'D', 'F', '']
    color = "\"red\""
    if grade not in fail:
       color = "\"green\"" 
    
    adviseButton = """
        <table class="t1" bgcolor="""+ color + """title=""" + className + """>
                        <tr>
                            <td></td>
                            <td><h3>"""+ className + """</h3></td>
                            <td></td>
                        </tr>
                        <tr>
                            
                            <td>
                                <form action="students" name="gradebutton" method="POST" onsubmit="return confirm()">
                                    <input type="hidden" id="""+ student_name + """ name ="student_name" value="""+student_name+""">
                                    <input type="hidden" id="""+ "g_"+className + """ name ="in_Data" value="""+gradeFormat+""">
                                    <input type="hidden" id="""+ className + """ name="class_name" value="""+className+""">
                                    <input type="hidden" id="""+ className + """ name="button_type" value="G">
                                    <input class="gbtn" type="submit" id="""+className+""" name="""+className+""" value="G" onclick="getGrade(this)">
                                </form>
                            </td>
                            <td>
                            </td>
                            <td>
                                <form action="students" name="commentButton" method="POST" onsubmit="return confirm()">
                                    <input type="hidden" id="""+ student_name + """ name ="student_name" value="""+student_name+""">
                                    <input type="hidden" id="""+ "c_"+className+""" name="in_Data" value="""+ "\""+ commentFormat +"\""+""">
                                    <input type="hidden" id="""+ className + """ name="class_name" value="""+className+""">
                                    <input type="hidden" id="""+ className + """ name="button_type" value="C">
                                    <input class="cbtn" type="submit" name="""+className+""" value="C" onclick="getComment(this)">
                                </form>
                            </td>
                           
                        </tr>
                    </table>
        """
    return adviseButton