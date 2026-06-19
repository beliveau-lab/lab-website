#!/usr/bin/env python3
"""One-time seed: writes data/team.json from the content scraped off the live
Wix site. After this runs you manage the roster with site.py, not this file.

Each member's `photo` is a local path under images/team or images/alumni; the
`photo_remote` is the original wixstatic URL. The site renders `photo` and
silently falls back to `photo_remote` if the local file isn't there yet, so the
page looks correct immediately and becomes fully self-hosted once you run
download_images.py.
"""
import json, pathlib

W = "https://static.wixstatic.com/media/"

current = [
    {"name": "Brian Beliveau", "role": "PI", "pi": True,
     "degree": "PhD in Genetics, Harvard Medical School",
     "email": "beliveau@uw.edu", "pronouns": "he/him/his",
     "social": {"label": "@oligopain", "url": "https://bsky.app/profile/oligopain.bsky.social"},
     "photo": "images/team/brian_beliveau.png",
     "photo_remote": W + "b8abaf_8b5707e1f21f44619b04bd9c15a7b8c2~mv2.png/v1/crop/x_2,y_0,w_838,h_842/fill/w_400,h_400,al_c,q_85,enc_avif,quality_auto/profile_crop3.png"},
    {"name": "Sahar Attar", "role": "Graduate Student (GS)",
     "email": "sahar60@uw.edu", "joined": "Jun 2023",
     "joint": {"name": "Schweppe Lab", "url": "https://www.schweppelab.org/"},
     "photo": "images/team/sahar_attar.jpg",
     "photo_remote": W + "b8abaf_cd269df7dfd0428da300fe2efcaca167~mv2.jpg/v1/crop/x_495,y_200,w_2467,h_2481/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_0504.jpg"},
    {"name": "Conor Camplisson", "role": "Graduate Student (GS)",
     "email": "concamp@uw.edu", "joined": "Jun 2020",
     "photo": "images/team/conor_camplisson.png",
     "photo_remote": W + "b8abaf_8b5707e1f21f44619b04bd9c15a7b8c2~mv2.png/v1/crop/x_2,y_0,w_838,h_842/fill/w_400,h_400,al_c,q_85,enc_avif,quality_auto/profile_crop3.png"},
    {"name": "Eanya Devasagayam", "role": "Undergraduate Researcher",
     "email": "eanyad@uw.edu", "program": "UW Bioengineering", "joined": "Mar 2024",
     "photo": "images/team/eanya_devasagayam.jpg",
     "photo_remote": W + "b8abaf_63b14e3de0984ecf8f54decaee14193a~mv2.jpg/v1/crop/x_972,y_268,w_2483,h_2486/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/DSC_7889.jpg"},
    {"name": "Kiara Dote", "role": "Undergraduate Researcher",
     "email": "kdote2@uw.edu", "program": "UW Molecular Cellular and Developmental Biology", "joined": "Oct 2025",
     "photo": "images/team/kiara_dote.jpg",
     "photo_remote": W + "b8abaf_683b9fe0f8624dbaa1b3d6e6eb9f26ef~mv2.jpg/v1/crop/x_95,y_257,w_783,h_783/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_3241.jpg"},
    {"name": "Pratika Eswaran", "role": "Undergraduate Researcher",
     "email": "pve2@uw.edu", "program": "UW Computer Science", "joined": "Jul 2025",
     "photo": "images/team/pratika_eswaran.jpg",
     "photo_remote": W + "b8abaf_9cbf0562507145ad91f8a47d8b2a36f7~mv2.jpg/v1/crop/x_1687,y_1134,w_1889,h_1890/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_3057.jpg"},
    {"name": "Julia Glasser", "role": "MS Student (MSDS)",
     "email": "glasserj@uw.edu", "joined": "Sept 2025",
     "photo": "images/team/julia_glasser.jpg",
     "photo_remote": W + "b8abaf_763567f9a8db478f88ef041808e0068b~mv2.jpg/v1/crop/x_0,y_386,w_2316,h_2316/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_9908.jpg"},
    {"name": "Conor Herlihy", "role": "Postdoctoral Fellow",
     "degree": "PhD in Biology and Biotechnology, Worcester Polytechnic Institute",
     "email": "cherlihy@uw.edu", "joined": "Jul 2024",
     "joint": {"name": "Schweppe Lab", "url": "https://www.schweppelab.org/"},
     "photo": "images/team/conor_herlihy.jpg",
     "photo_remote": W + "b8abaf_38272f18d3374df7bca08b58ac8f472a~mv2.jpg/v1/crop/x_227,y_113,w_911,h_911/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_6503.jpg"},
    {"name": "Hunter Jung", "role": "Undergraduate Researcher",
     "email": "hjung17@uw.edu", "program": "UW French (Premed)", "joined": "Oct 2023",
     "joint": {"name": "Schweppe Lab", "url": "https://www.schweppelab.org/"},
     "photo": "images/team/hunter_jung.jpg",
     "photo_remote": W + "b8abaf_c4b2d9a82b9b493a90d18a50fa530ead~mv2.jpg/v1/crop/x_700,y_1135,w_1587,h_1587/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_0659.jpg"},
    {"name": "Conor Kelly", "role": "Graduate Student (GS)",
     "email": "cokelly@uw.edu", "joined": "Jun 2023",
     "photo": "images/team/conor_kelly.jpg",
     "photo_remote": W + "b8abaf_f2e7685fab1f4d23908bd20970733102~mv2.jpg/v1/crop/x_149,y_129,w_2382,h_2398/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/Conor_Kelly.jpg"},
    {"name": "Mary Krebs", "role": "Research Assistant",
     "email": "maryk88@uw.edu", "joined": "Sept 2022",
     "photo": "images/team/mary_krebs.jpg",
     "photo_remote": W + "b8abaf_b4289aa67b824f7cbb6278143283205e~mv2.jpg/v1/crop/x_44,y_262,w_2220,h_2233/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_8236.jpg"},
    {"name": "Lidan Li", "role": "Postdoctoral Fellow",
     "degree": "PhD in Chemical Engineering and Technology, Beijing University of Chemical Technology",
     "email": "lidanl@uw.edu", "joined": "Mar 2024",
     "photo": "images/team/lidan_li.jpg",
     "photo_remote": W + "b8abaf_580f7c4c471941ccad9dddfc9627d7a9~mv2.jpg/v1/crop/x_0,y_206,w_1634,h_1634/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/Lidan%20Li.jpg"},
    {"name": "Nicolas Longhi", "role": "Research Assistant",
     "email": "longnic@uw.edu", "joined": "Jun 2023",
     "photo": "images/team/nicolas_longhi.jpg",
     "photo_remote": W + "b8abaf_b67e295071c0472f94675f3a417d32b5~mv2.jpg/v1/crop/x_105,y_809,w_2459,h_2471/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_6209.jpg"},
    {"name": "Aadyant Maity", "role": "Undergraduate Researcher",
     "email": "amaity@uw.edu", "program": "UW Computer Science", "joined": "Aug 2025",
     "photo": "images/team/aadyant_maity.jpg",
     "photo_remote": W + "b8abaf_b40e24ca6d6d4e60a5fecac9f235bb0e~mv2.jpeg/v1/crop/x_55,y_0,w_2592,h_2592/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_7489.jpeg"},
    {"name": "Arin Meeks-Muradyan", "role": "Undergraduate Researcher",
     "email": "arinmks@uw.edu", "program": "UW Bioengineering", "joined": "Jul 2025",
     "photo": "images/team/arin_meeks_muradyan.jpg",
     "photo_remote": W + "b8abaf_69a603c238ef40acb1d738740dcd0199~mv2.jpg/v1/crop/x_256,y_153,w_541,h_541/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/IMG_9663.jpg"},
    {"name": "Eva K. Nichols", "role": "Acting Instructor",
     "degree": "PhD in Molecular and Cell Biology, UC Berkeley",
     "email": "eknich@uw.edu", "pronouns": "she/her", "joined": "Jul 2020",
     "social": {"label": "@evaknichols", "url": "https://twitter.com/evaknichols"},
     "joint": {"name": "Shendure Lab", "url": "https://shendure-web.gs.washington.edu/"},
     "photo": "images/team/eva_nichols.jpg",
     "photo_remote": W + "b8abaf_0f0d1822d49147459a15bf22b0cd6f51~mv2.jpg/v1/crop/x_28,y_0,w_919,h_918/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/Image%20from%20iOS%20(3).jpg"},
    {"name": "Monika Perez", "role": "Graduate Student (GS)",
     "email": "mwperez@uw.edu", "joined": "Jun 2023",
     "photo": "images/team/monika_perez.jpg",
     "photo_remote": W + "b8abaf_eb9a0b9567364ff8b47d7a6125584423~mv2.jpg/v1/crop/x_118,y_0,w_956,h_961/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/10-03-17%20monika%20perez_headshot.jpg"},
    {"name": "Madison Sanchez-Forman", "role": "MS Student (MSDS)",
     "email": "msforman@uw.edu", "pronouns": "she/her/hers", "joined": "Sept 2024",
     "photo": "images/team/madison_sanchez_forman.png",
     "photo_remote": W + "b8abaf_680b1c25e7df46cea995ad16a8f8df9b~mv2.png/v1/crop/x_765,y_1587,w_2711,h_2714/fill/w_400,h_400,al_c,q_85,enc_avif,quality_auto/IMG_0291_HEIC.png"},
    {"name": "Olivia Weissenfels", "role": "Rotation Student (GS)",
     "email": "Opodha@uw.edu", "joined": "Sept 2025",
     "photo": "images/team/olivia_weissenfels.jpg",
     "photo_remote": W + "b8abaf_db31bfdaec214784917857b02afb9f1c~mv2.jpg/v1/crop/x_0,y_113,w_2083,h_2083/fill/w_400,h_400,al_c,q_80,enc_avif,quality_auto/OliviaWeissenfels.jpg"},
]

# Alumni: name, role, dates, after (current position), photo_remote (120x125 crop kept)
alumni = [
    ("David Nwizugbo", "Research Assistant", "Apr 2022 – Sept 2025", "Now an MS Student at Queen Mary University of London", "https://www.qmul.ac.uk/postgraduate/taught/coursefinder/courses/molecular-cell-biology-msc/", "b8abaf_0a44d45f49d14693a9701084bfedbf2e~mv2.jpg/v1/crop/x_0,y_57,w_602,h_627/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/websitephoto.jpg"),
    ("Valentino (Val) Browning", "Research Assistant", "Nov 2021 – Sept 2025", "Now a PhD Student in the MCB Program", "https://mcb-seattle.edu/", "b8abaf_f5775c8691cd41dc969a23ec2338135e~mv2.png/v1/crop/x_0,y_63,w_254,h_264/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/pic1.png"),
    ("Gulnar Albushova", "MS Student (Berkeley Data Science)", "Jun 2025 – Jul 2025", None, None, "b8abaf_27d6f2d3fac8450994e9998016cfbfd9~mv2.jpg/v1/crop/x_3,y_451,w_613,h_637/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/web%20picture.jpg"),
    ("Vincent Chau", "Undergraduate Researcher", "Jul 2023 – May 2025", None, None, "b8abaf_16d63a755dc644fba0b0cc133bd7f383~mv2.png/v1/crop/x_48,y_0,w_2304,h_2400/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/Vincent%20C.png"),
    ("Ben Scott", "Summer Undergraduate Researcher", "Jun 2025 – Aug 2025", None, None, "b8abaf_0c29902b6f094153b2209e10ea4ce0d5~mv2.png/v1/crop/x_150,y_54,w_379,h_395/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/image%20(26).png"),
    ("Chelsey Lin", "Research Assistant", "Jun 2022 – Jul 2025", "Now a PhD student in the Rice Bioengineering program", "https://bioengineering.rice.edu/academics/phd-program", "b8abaf_1295350419584da0b9fc2853917b4dfd~mv2.jpg/v1/crop/x_674,y_192,w_597,h_621/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/%E6%9D%A5%E8%87%AA%20iOS%20%E7%9A%84%E5%9B%BE%E5%83%8F.jpg"),
    ("Yuzhen Liu", "Graduate Student (GS)", "Jun 2020 – Mar 2025", "Now a Scientist I at Allen Institute for Neural Dynamics", "https://alleninstitute.org/division/neural-dynamics/", "b8abaf_b5bb3c2749524003a1051a96c12d4c3d~mv2.jpeg/v1/crop/x_363,y_0,w_856,h_890/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Yuzhen_Liu_headshot.jpeg"),
    ("Eric Lian", "Undergraduate Researcher", "Sept 2024 – Feb 2025", None, None, "b8abaf_a5add8d235c4432c836f21707b7c20c2~mv2.jpg/v1/crop/x_543,y_806,w_1470,h_1529/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/ELian_JPG.jpg"),
    ("Lawrie Brunswick", "MS Student (MSDS)", "Sept 2023 – Dec 2024", None, None, "b8abaf_b8a7c01a8fe945b9ac55b72e3c587e5c~mv2.jpeg/v1/crop/x_59,y_0,w_1682,h_1752/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Polish_20200906_144223573.jpeg"),
    ("Nicole Hang", "Summer Undergraduate Researcher", "Jun 2024 – Aug 2024", None, None, "b8abaf_dca09ac672c54e76b081e4f1cd89226d~mv2.jpg/v1/crop/x_323,y_172,w_1291,h_1345/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_8858.jpg"),
    ("Jaden Mattison", "Summer Undergraduate Researcher", "Jun 2024 – Aug 2024", None, None, "b8abaf_6102493f60c24219945f92c59b22d467~mv2.jpg/v1/crop/x_58,y_115,w_1195,h_1246/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/P1010013.jpg"),
    ("Matthew Chaw", "Rotation Student (GS)", "Sept 2023 – Dec 2023", None, None, "b8abaf_8bd579b69c5e4f95a4f526b5c32d8635~mv2.jpg/v1/crop/x_79,y_19,w_498,h_519/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/20220930%20Matthew%20Chaw%2064960%200518%20648%20(1).jpg"),
    ("Robin Aguilar", "Graduate Student (GS)", "Jun 2019 – Nov 2023", "Now a Science Communication Specialist at A-Alpha Bio", "https://www.aalphabio.com/", "b8abaf_4e2463c93e4d4469b579ad1a7b0f5363~mv2.jpg/v1/crop/x_943,y_970,w_1194,h_1244/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_5236_JPG.jpg"),
    ("Caleb Kono", "Undergraduate Researcher", "Jun 2022 – Sept 2023", "Now a PhD student in the UW BPSD program", "https://depts.washington.edu/bpsd/", "b8abaf_f537f23786b543b98464b6800b5c19da~mv2.jpg/v1/crop/x_454,y_55,w_483,h_502/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/8265D3DF-7F29-404A-8F6F-B35C49F02521.jpg"),
    ("Chandler Ault", "MS Student (MSDS)", "Oct 2022 – Jul 2023", "Now an intern at Exponential", "https://xpn.ai/", "b8abaf_60bbe04c58984bb0b5b1403b6de2b7ed~mv2.png/v1/crop/x_5,y_5,w_259,h_266/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/beliveau.png"),
    ("Stephen Gonzalez", "GS Rotation Student", "Apr 2023 – Jun 2023", "Now a Graduate Student in the Trapnell Lab", None, "b8abaf_6a1e2f3c8e2d4a49abf3489a9eaeecbb~mv2.jpg/v1/crop/x_0,y_64,w_1125,h_1143/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/8F218844-9CDF-485A-9686-CD5FCEF10EF3%202.jpg"),
    ("Thomas A. Perkins, Jr.", "Research Assistant", "Sept 2022 – Mar 2023", None, None, "b8abaf_d6d9ed3c539449de85c4a157d4ba3abf~mv2.jpg/v1/crop/x_400,y_228,w_962,h_975/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_1941.jpg"),
    ("Connor Finkbeiner", "GS Rotation Student", "Jan 2023 – Mar 2023", "Now a Graduate Student in the Setty Lab", "https://research.fredhutch.org/setty/en.html", "b8abaf_1e9ca347553042469ef19e8e732bbc1b~mv2.png/v1/crop/x_366,y_353,w_902,h_918/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/MicrosoftTeams-image%20(3).png"),
    ("Conor Kelly", "GS Rotation Student", "Jan 2023 – Mar 2023", "Now a Graduate Student in the Beliveau Lab (!)", None, "b8abaf_f2e7685fab1f4d23908bd20970733102~mv2.jpg/v1/crop/x_0,y_83,w_2596,h_2638/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Conor_Kelly.jpg"),
    ("Monika Perez", "GS Rotation Student", "Sept 2022 – Dec 2022", "Now a Graduate Student in the Beliveau Lab (!)", None, "b8abaf_eb9a0b9567364ff8b47d7a6125584423~mv2.jpg/v1/crop/x_176,y_0,w_828,h_841/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/10-03-17%20monika%20perez_headshot.jpg"),
    ("Sahar Attar", "GS Rotation Student", "Sept 2022 – Dec 2022", "Now a Graduate Student in the Beliveau and Schweppe Labs (!)", "https://www.schweppelab.org/", "b8abaf_cd269df7dfd0428da300fe2efcaca167~mv2.jpg/v1/crop/x_671,y_179,w_2054,h_2092/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_0504.jpg"),
    ("Sahar Attar", "Research Assistant", "Feb 2020 – Sept 2022", "Now a PhD student in the UW Genome Sciences program", None, "b8abaf_cd269df7dfd0428da300fe2efcaca167~mv2.jpg/v1/crop/x_671,y_179,w_2054,h_2092/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_0504.jpg"),
    ("Melissa Phung-Rojas", "Summer Undergraduate Researcher", "May 2022 – Aug 2022", None, None, "b8abaf_cfc0edab8ee747a990de245b22af45f4~mv2.png/v1/crop/x_335,y_711,w_534,h_542/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/Image%20from%20iOS.png"),
    ("Saurabh Shukla", "Visiting Postdoctoral Fellow", "Jul 2021 – Jun 2022", "Now a Data Scientist at Prescryptive Health", "https://prescryptive.com/", "b8abaf_7ea7cdbaa817402eae99162f93b8fd95~mv2.jpeg/v1/crop/x_43,y_26,w_463,h_466/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/SaurabhShukla.jpeg"),
    ("Benjamin Mallory", "GS Rotation Student", "Mar 2022 – Jun 2022", "Now a Graduate Student in the Starita Lab and the Stergachis Lab", None, "b8abaf_645dd66530044c85a5c94dabef9e4707~mv2.jpg/v1/crop/x_0,y_65,w_1908,h_1923/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Headshot.jpg"),
    ("Chris Hsu", "Graduate Student (GS)", "Jun 2021 – Mar 2022", "Now a Graduate Student in the MacCoss Lab", "https://www.maccosslab.org/", "b8abaf_aec97330b4434b2d9b3e3e5bf03d72e6~mv2.jpg/v1/crop/x_67,y_36,w_624,h_622/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_2689.jpg"),
    ("Lily Deng", "Staff Engineer", "Sept 2018 – Mar 2022", "Now a Computational Biology Scientist at RareCyte", "https://rarecyte.com/", "b8abaf_434a42ffab304f38ad2e22b436bd6e74~mv2.png/v1/crop/x_1,y_0,w_238,h_240/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/lily-picture-3.png"),
    ("Malvika Tejura", "GS Rotation Student", "Jan 2022 – Mar 2022", "Now a Graduate Student in the Fowler Lab and the Starita Lab", "https://fowlerlab.gs.washington.edu/", "b8abaf_e4676f3e8d4947b0babc468429341fc3~mv2.jpg/v1/crop/x_1133,y_0,w_4438,h_4474/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Image%20from%20iOS.jpg"),
    ("Connor Kubo", "GS Rotation Student", "Sept 2021 – Dec 2021", "Now a Graduate Student in the Shendure Lab", "https://shendure-web.gs.washington.edu/", "b8abaf_5162456e3e934752b920ef21d0474bba~mv2.jpg/v1/crop/x_0,y_137,w_727,h_727/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Image%20from%20iOS%20(6).jpg"),
    ("Shruti Jain", "GS Rotation Student", "Sept 2021 – Dec 2021", "Now a Graduate Student in the Baker Lab and the Shendure Lab", "https://www.bakerlab.org/", "b8abaf_fb7af1c8193c4974ae6b1d4c8026b31d~mv2.jpeg/v1/crop/x_122,y_0,w_836,h_836/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/ShrutiJainPicture.jpeg"),
    ("Sneh Gupta", "Undergraduate Researcher", "Jun 2021 – Dec 2021", "Now an MS student in the Georgia Tech Master's Computer Science program", "https://www.cc.gatech.edu/degree-programs/master-science-computer-science", "b8abaf_58f8948610e84590b94376de9441ec8f~mv2.png/v1/crop/x_54,y_1,w_874,h_879/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/image%20(18).png"),
    ("Caleb Bower", "GS Summer REU Researcher", "Jun 2021 – Aug 2021", None, None, "b8abaf_c3f731fb8cb34b81bd32dd5ddf534c29~mv2.jpg/v1/crop/x_62,y_29,w_254,h_254/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Linkedin_JPG.jpg"),
    ("Ryan Chern", "Undergraduate Researcher", "Nov 2019 – Jun 2021", None, None, "b8abaf_ff4f97ad82874022bfc63ee7a6f51695~mv2_d_1281_1281_s_2.png/v1/crop/x_5,y_0,w_1271,h_1281/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/ryanchern.png"),
    ("Melissa Phung-Rojas", "Summer Undergraduate Researcher", "May 2021 – Aug 2021", None, None, "b8abaf_cfc0edab8ee747a990de245b22af45f4~mv2.png/v1/crop/x_337,y_709,w_545,h_544/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/Image%20from%20iOS.png"),
    ("Chris Hsu", "GS Rotation Student", "Jan 2021 – Mar 2021", "Now a Graduate Student in the MacCoss Lab", "https://www.maccosslab.org/", "b8abaf_aec97330b4434b2d9b3e3e5bf03d72e6~mv2.jpg/v1/crop/x_67,y_36,w_624,h_622/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_2689.jpg"),
    ("Lincoln Harris", "GS Rotation Student", "Mar 2021 – Jun 2021", "Now a Graduate Student in the Noble Lab", None, "b8abaf_658692ad466b4200ae6307156a574f1a~mv2.png/v1/crop/x_0,y_160,w_686,h_687/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/ljh_headshot.png"),
    ("Shayan Avanessian", "MCB Rotation Student", "Jan 2021 – Mar 2021", "Now a Graduate Student in the Barry Lab", "https://research.fredhutch.org/barry/en.html", "b8abaf_6df9d7f24df24c5a9cb5ba52057c8f2f~mv2.jpg/v1/crop/x_289,y_252,w_920,h_921/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Shayan_broadheadshot.jpg"),
    ("Jackson Zariski", "Undergraduate Researcher", "Feb 2019 – Mar 2021", "Now a PhD student in the University of Arizona Applied Mathematics program", "https://appliedmath.arizona.edu/", "b8abaf_b35e037def9e4ccc8f7119b3ee2d0311~mv2.png/v1/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/Jackson.png"),
    ("Alisa Tvorun-Dunn", "Undergraduate Researcher", "Jan 2019 – Mar 2021", "Now an MS student in the Dartmouth Quantitative Biological Sciences program", "https://geiselmed.dartmouth.edu/qbs/", "b8abaf_5192317481b344159090bdcd76aced16~mv2.png/v1/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/Alisa.png"),
    ("Leah Anderson", "GS Rotation Student", "Sept 2020 – Dec 2020", "Now a Graduate Student in the Dunham Lab", "https://dunham.gs.washington.edu/", "b8abaf_680646f7a95d463e96ce9273420029a7~mv2.jpg/v1/crop/x_0,y_156,w_761,h_761/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/leah_headshot.jpg"),
    ("Aidan Keith", "GS Rotation Student", "Sept 2020 – Dec 2020", "Now a Graduate Student in the Shendure Lab", "https://shendure-web.gs.washington.edu/", "b8abaf_d9e76b51ff974de2984dc80f14a79da1~mv2.jpg/v1/crop/x_0,y_106,w_1725,h_1725/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/AK_Photo.jpg"),
    ("Jumana Fathima", "Summer Undergraduate Researcher", "Jun 2020 – Sept 2020", "Now a Computational Biologist at Dyno Therapeutics", "https://www.dynotx.com/", "b8abaf_bb8e95467c80486fb8662d65ba1f09a8~mv2.png/v1/crop/x_44,y_15,w_363,h_363/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/headshot_jumana.png"),
    ("Elliot Hershberg", "Postbaccalaureate Researcher & Research Assistant", "Sept 2018 – Jun 2020", "Now a PhD student in the Stanford Genetics program and BDFL of PaintSHOP", None, "b8abaf_cb3d13506f174d94b7a238d18d98bc47~mv2.png/v1/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/elliot_hershberg_portrait_photo_240.png"),
    ("Zorian Thornton", "GS Rotation Student", "Mar 2020 – Jun 2020", "Now a Graduate Student in the Matsen Lab and honorary Beliveau Lab member =)", None, "b8abaf_b1607ef8117a430fb1b5e41dae4c9f06~mv2.jpg/v1/crop/x_234,y_208,w_925,h_927/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/recomb19-min_JPG.jpg"),
    ("Conor Camplisson", "GS Rotation Student", "Sept 2019 – Dec 2019", "Now a Graduate Student in the Beliveau Lab (!)", None, "b8abaf_8b5707e1f21f44619b04bd9c15a7b8c2~mv2.png/v1/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/profile_crop3.png"),
    ("Yuzhen Liu", "MCB Rotation Student", "Sept 2019 – Dec 2019", "Now a Graduate Student in the Beliveau Lab (!)", None, "b8abaf_b5bb3c2749524003a1051a96c12d4c3d~mv2.jpeg/v1/crop/x_367,y_0,w_892,h_890/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Yuzhen_Liu_headshot.jpeg"),
    ("Soyeon Showman", "MCB Rotation Student", "Sept 2019 – Dec 2019", "Now a Graduate Student in the Henikoff Lab and frequent Beliveau Lab visitor =)", "https://research.fredhutch.org/henikoff/en.html", "b8abaf_bebadcccdea74ed391a531c62281280c~mv2_d_2132_2064_s_2.jpg/v1/crop/x_310,y_231,w_1395,h_1395/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/Soyeon%20Showman_JPG.jpg"),
    ("Robin Aguilar", "GS Rotation Student", "Apr 2019 – Jun 2019", "Now a Graduate Student in the Beliveau and Noble Labs (!)", None, "b8abaf_cf7954cde20d4bac8199aa5c0ecf58e4~mv2_d_4032_3024_s_4_2.jpg/v1/crop/x_504,y_0,w_3024,h_3024/fill/w_240,h_250,al_c,q_80,enc_avif,quality_auto/IMG_0463.jpg"),
    ("Amy Xu", "Undergraduate Researcher", "Sept 2018 – May 2019", None, None, "b8abaf_bdb58a5ab2c04292a881e3868f8629cc~mv2.png/v1/fill/w_240,h_250,al_c,q_85,enc_avif,quality_auto/amyxu.png"),
]

def slug(name, dates):
    base = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace(",", "").replace("/", "_")
    return base

alumni_out = []
for name, role, dates, after, after_url, remote in alumni:
    rec = {"name": name, "role": role, "dates": dates,
           "photo": f"images/alumni/{slug(name, dates)}.jpg",
           "photo_remote": W + remote}
    if after:
        rec["after"] = after
    if after_url:
        rec["after_url"] = after_url
    alumni_out.append(rec)

data = {"current": current, "alumni": alumni_out}
out = pathlib.Path(__file__).resolve().parent.parent / "data" / "team.json"
out.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print(f"Wrote {out} — {len(current)} current, {len(alumni_out)} alumni")
