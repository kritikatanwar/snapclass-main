import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects,get_attendance_for_teacher
from src. components.dialog_create_subject import create_subject_dialog
from src. components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photos import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
from datetime import datetime
from src.components.dialog_attendance_results import attendance_results_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog


def teacher_screen():
    style_background_dashboard()
    style_base_layout()
   
    if "teacher_data" in st.session_state:
         teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
         teacher_screen_login()  
    elif st.session_state.teacher_login_type=="register":
         teacher_screen_register()
         

def teacher_dashboard():
    teacher_data= st.session_state.teacher_data
    c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
         header_dashboard()
    with c2:
         st.subheader(f""" Welcome,{teacher_data['name']}!""")
         if st.button('Logout', type='secondary',key='loginbckbtn',shortcut="control + backspace"):
               st.session_state['is_logged_in']= False
               del st.session_state.teacher_data
               st.rerun()
    st.space()
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'
    tab1,tab2,tab3= st.columns(3)

    with tab1:
        type1= "primary" if st. session_state.current_teacher_tab== 'take_attendance' else"tertiary"
        if st.button('Take Attendance',type = type1, width='stretch', icon=':material/ar_on_you:'):
           st. session_state. current_teacher_tab = 'take_attendance'
           st.rerun()

    with tab2:
       type2= "primary" if st. session_state.current_teacher_tab==  'manage_subjects' else"tertiary"
       if st.button('Manage Subjects',type = type2, width='stretch', icon=':material/book_ribbon:'):
           st. session_state. current_teacher_tab = 'manage_subjects'
           st.rerun()

    with tab3:
       type3= "primary" if st. session_state.current_teacher_tab== 'attendance_records' else"tertiary"
       if st.button('Attendance Records',type = type3, width='stretch', icon=':material/cards_stack:'):
           st. session_state. current_teacher_tab = 'attendance_records'
           st.rerun()
    
    st.divider()
    if st.session_state.current_teacher_tab =="take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab =="manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab =="attendance_records":
        teacher_tab_attendance_records()   



    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id= st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]

    subjects= get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('Yoy have not created any subjects yet! Please create one to begin!')
        return
    
    subject_options= {f"{s['name']} - {s['subject_code']}":s['subject_id'] for s in subjects}
    
    col1, col2 = st.columns([4, 1.3], vertical_alignment="bottom")

    with col1:
      selected_subject_label= st.selectbox(
        "Select Subject",
        subject_options
    )

    with col2:
       if st.button(
        "Add Photos",
        type="primary",
        use_container_width=True,icon=":material/add_photo_alternate:",
    ):
        
        add_photos_dialog()
    selected_subject_id= subject_options[selected_subject_label]
 

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1,c2,c3= st.columns(3)
    with c1:
        if st.button('Clear all photos',width='stretch',type='tertiary',icon=':material/delete:',disabled= not has_photos):
            st.session_state.attendance_images=[]
            st.rerun()

    with c2:
        has_photos=bool(st.session_state.attendance_images)
        if st.button('Run Face Analysis',width='stretch',type='secondary',icon=':material/analytics:',disabled= not has_photos):
            with st.spinner("Deep Scanning classroom photos..."):
                all_detected_id={}
                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np= np.array(img.convert('RGB'))

                    detected,_,_= predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id= int(sid)
                            all_detected_id.setdefault(student_id,[]).append(f"Photo{idx+1}")


                enrolled_res= supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()
                enrolled_students=enrolled_res.data
                if not  enrolled_students:
                    st.warning('No students in this course')
                else:
                    results,attendance_to_log= [],[] 
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in  enrolled_students:
                        student= node['students']
                        sources = all_detected_id.get(int(student["student_id"]), [])
                        is_present = len(sources) > 0

                        results.append({
                             "Name": student['name'],
                             "ID":student['student_id'],
                             "Source":",".join(sources) if is_present else "-",
                             "Status":" ✅Present" if is_present else "❌ Absent"
                           })
                        
                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_results_dialog(pd.DataFrame(results), attendance_to_log)
    with c3:
      if st.button('Use Voice Attendance', type='primary', width='stretch', icon=":material/mic:"):
          voice_attendance_dialog(selected_subject_id)





    
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')
    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)
    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
   
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                     share_subject_dialog(sub['name'], sub['subject_code'])
                     st.space()

            subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats=stats,
            footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header("Attendance Records")

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found.")
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(
            ['ts_group', 'Time', 'Subject', 'Subject Code']
        )
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ "
        + summary['Present_Count'].astype(str)
        + " / "
        + summary['Total_Count'].astype(str)
        + " Students"
    )

    display_df = (
        summary.sort_values(
            by='ts_group',
            ascending=False
        )[
            ['Time', 'Subject', 'Subject Code', 'Attendance Stats']
        ]
    )

    # ---------------- SEARCH + FILTER ----------------

    c1, c2 = st.columns([3, 1])

    with c1:
        search_term = st.text_input(
            "",
            placeholder="🔍 Search subject..."
        )

    with c2:
        selected_subject = st.selectbox(
            "",
            ["All Subjects"]
            + sorted(display_df["Subject"].unique().tolist())
        )

    filtered_df = display_df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df["Subject"].str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    if selected_subject != "All Subjects":
        filtered_df = filtered_df[
            filtered_df["Subject"] == selected_subject
        ]

    # ---------------- AG GRID ----------------

    gb = GridOptionsBuilder.from_dataframe(filtered_df)

    gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True
    )

    gb.configure_column(
        "Time",
        width=250
    )

    gb.configure_column(
        "Subject",
        width=280
    )

    gb.configure_column(
        "Subject Code",
        width=140
    )

    gb.configure_column(
        "Attendance Stats",
        width=220
    )

    gb.configure_grid_options(
        rowHeight=55,
        headerHeight=55,
        animateRows=True
    )

    grid_options = gb.build()

    
    custom_css = {
    ".ag-root-wrapper": {
        "border": "2px solid #cfd5ff",
        "border-radius": "20px",
        "overflow": "hidden",
    },
    ".ag-header": {
        "background-color": "#5C6CFF !important",
        "color": "white !important",
        "font-weight": "bold"
    },

    # Table body
    ".ag-center-cols-container": {
        "background-color": "#EEF0FF"
    },

    # Individual rows
    ".ag-row": {
        "background-color": "#EEF0FF",
        "font-size": "15px"
    },

    # Hover effect
    ".ag-row-hover": {
        "background-color": "#E3E7FF !important"
    }
}
    
    
    AgGrid(
    filtered_df,
    gridOptions=grid_options,
    custom_css=custom_css,
    theme="material",
    height=min(600, 55 + len(filtered_df) * 55),
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True
   )

   

   




def login_teacher(teacher_username,teacher_pass):
    if not teacher_username or not teacher_pass:
        return False
    teacher= teacher_login(teacher_username,teacher_pass)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in= True
        return True
    
    return False


def teacher_screen_login():
      c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
      with c1:
         header_dashboard()
      with c2:
         if st.button('Go Back To Home', type='secondary',key='loginbckbtn',shortcut="control + backspace"):
               st.session_state['login_type']=None
               st.rerun()
        
      st.header("Login using password", text_alignment='center')
      st.space()
      st.space()
      
      teacher_username= st.text_input("Enter username", placeholder='kritikatanwar')
      teacher_pass= st.text_input("Enter your passowrd",type= 'password',placeholder='Enter password')
      st.divider()

      btnc1,btnc2=st.columns(2)
      with btnc1:
          if st.button('Login', icon=':material/passkey:',shortcut="control + enter",width='stretch'):
              if login_teacher(teacher_username,teacher_pass):
                  st.toast("Welcome Back!", icon="👋🏻")
                  import time
                  time.sleep(1)
                  st.rerun()
              else:
                  st.error("Invalid username and password combo! Please check")

      with btnc2:
           if st.button('Register Instead', icon=':material/passkey:',type='primary',width='stretch'):
                st.session_state.teacher_login_type="register"
                st.rerun()
      footer_dashboard()


def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False,"All fields are required!"
    if check_teacher_exists(teacher_username):
        return False,"Username already exists"
    if teacher_pass!=teacher_pass_confirm:
        return False,"Password doesn't match"
    
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Sucessfuly registered,Login Now!"
    except Exception as e:
        return False,"Unexpected Error!"
    

def teacher_screen_register():
      c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
      with c1:
         header_dashboard()
      with c2:
         if st.button('Go Back To Home', type='secondary',key='loginbckbtn',shortcut="control + backspace"):
               st.session_state['login_type']=None
               st.rerun()
      st.header("Register your teacher profile")
      st.space()
      st.space()
      teacher_username= st.text_input("Enter username", placeholder='kritikatanwar')
      teacher_name= st.text_input("Enter your name", placeholder='Kritika Tanwar')
      teacher_pass= st.text_input("Enter your passowrd",type= 'password',placeholder='Enter password')
      teacher_pass_confirm= st.text_input("Confirm your passowrd",type= 'password',placeholder='Enter password')
      st.divider()

      btnc1,btnc2=st.columns(2)
      with btnc1:
         if  st.button('Register Now', icon=':material/passkey:',shortcut="control + enter",width='stretch',type='primary'):
             success,message= register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
             if success:
                st.success(message) #green box with message appears
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login" # as we move to login page automatically after registeration 
                st.rerun()
             else:
                st.error(message)

      with btnc2:
           if st.button('Login Instead', icon=':material/passkey:',width='stretch'):
             st.session_state.teacher_login_type="login"
             st.rerun()
      footer_dashboard()

