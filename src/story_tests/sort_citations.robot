*** Settings ***
Resource  resource.robot
Library         SeleniumLibrary
Library         Collections
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Thirty Test Citations And Go To Home Page

*** Test Cases ***

Sort By Title Ascending
    Sort Title Ascending
    ${first_title}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]//a
    Should Contain  ${first_title}  Agile Methodology

Sort By Title Descending
    Sort Title Ascending
    Sort Title Descending
    ${first_title}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]//a
    Should Contain  ${first_title}  Web Development Guide

Sort By Year Ascending
    Sort Year Ascending
    ${first_year}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]/td[3]
    Should Be Equal  ${first_year}  2000

Sort By Year Descending
    Sort Year Ascending
    Sort Year Descending
    ${first_year}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]/td[3]
    Should Be Equal  ${first_year}  2024

Sort By Type Ascending
    Sort Type Ascending
    ${first_type}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]/td[2]
    Should Be Equal  ${first_type}  article

Sort By Type Descending
    Sort Type Ascending
    Sort Type Descending
    ${first_type}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]/td[2]
    Should Be Equal  ${first_type}  misc

Triple Click Resets Sort Order
    Sort Title Ascending
    Sort Title Descending
    Click Element  xpath=//th[contains(text(), 'Title')]
    ${indicator_text}=  Get Text  xpath=//span[@id='sort-indicator-title']
    Should Be Empty  ${indicator_text}
    ${first_title}=  Get Text  xpath=//tbody[@id='citations-tbody']/tr[1]//a
    Should Contain  ${first_title}  Machine Learning Fundamentals

*** Keywords ***

Reset Citations Create Thirty Test Citations And Go To Home Page
    Reset Citations
    Create Thirty Test Citations
    Go To Home Page

Sort Title Ascending
    Click Element  xpath=//th[contains(text(), 'Title')]
    Wait Until Page Contains Element  xpath=//span[@id='sort-indicator-title' and contains(text(), '▲')]

Sort Title Descending
    Click Element  xpath=//th[contains(text(), 'Title')]
    Wait Until Page Contains Element  xpath=//span[@id='sort-indicator-title' and contains(text(), '▼')]

Sort Year Ascending
    Click Element  xpath=//th[contains(text(), 'Year')]
    Wait Until Page Contains Element  xpath=//span[@id='sort-indicator-year' and contains(text(), '▲')]

Sort Year Descending
    Click Element  xpath=//th[contains(text(), 'Year')]
    Wait Until Page Contains Element  xpath=//span[@id='sort-indicator-year' and contains(text(), '▼')]

Sort Type Ascending
    Click Element  xpath=//th[contains(text(), 'Type')]
    Wait Until Page Contains Element  xpath=//span[@id='sort-indicator-type' and contains(text(), '▲')]

Sort Type Descending
    Click Element  xpath=//th[contains(text(), 'Type')]
    Wait Until Page Contains Element  xpath=//span[@id='sort-indicator-type' and contains(text(), '▼')]