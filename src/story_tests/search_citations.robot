*** Settings ***
Resource  resource.robot
Library         SeleniumLibrary
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Thirty Test Citations And Go To Home Page

*** Test Cases ***

Search By Title Filters Citations
    Search For                           Machine Learning
    Wait Until Page Contains             Machine Learning Fundamentals
    Page Should Contain                  Machine Learning Fundamentals
    Visible Citation Row Count Should Be  1

Search By Year Filters Citations
    Search For                           2005
    Visible Citation Row Count Should Be At Least  1

Search With No Results Shows No Citations
    Search For                           NonExistentTitle12345
    Visible Citation Row Count Should Be  0

Clear Search Restores All Citations
    Search For                           Machine Learning
    Visible Citation Row Count Should Be  1
    Clear Search
    Visible Citation Row Count Should Be  30

Search Is Case Insensitive
    Search For                           machine learning
    Page Should Contain                  Machine Learning Fundamentals
    Visible Citation Row Count Should Be  1

*** Keywords ***

Reset Citations Create Thirty Test Citations And Go To Home Page
    Reset Citations
    Create Thirty Test Citations
    Go To Home Page

Search For
    [Arguments]    ${query}
    Input Text     id=search-input    ${query}

Get Visible Citation Rows
    ${visible_rows}=    Get WebElements
    ...    xpath=//tr[contains(@class, 'citation-row') and not(contains(@style, 'display: none'))]
    [Return]            ${visible_rows}

Visible Citation Row Count Should Be
    [Arguments]    ${expected}
    ${visible_rows}=    Get Visible Citation Rows
    Length Should Be    ${visible_rows}    ${expected}

Visible Citation Row Count Should Be At Least
    [Arguments]    ${minimum}
    ${visible_rows}=    Get Visible Citation Rows
    Should Be True      ${visible_rows.__len__()} >= ${minimum}

Clear Search
    Clear Element Text  id=search-input
    Press Keys          id=search-input    RETURN
