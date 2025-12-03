*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Test Citation And Go To Home Page

*** Test Cases ***

Click Citation Title
    Click Link  Testilähde
    Page Should Contain  Details
    Page Should Contain  Title: Testilähde
    Page Should Contain  Author: Testitekijä
    Page Should Contain  Year: 1900

Navigate Back To Home Screen
    Click Link  Testilähde
    Page Should Contain  Details
    Scroll Element Into View    id=back-btn
    Wait Until Element Is Visible    id=back-btn
    Click Element    id=back-btn
    Page Should Contain  Create new citation

Delete Citation
    Click Link    Testilähde
    Page Should Contain    Details
    Scroll Element Into View    id=delete-btn
    Wait Until Element Is Visible    id=delete-btn
    Click Button    delete-btn
    Handle Alert    ACCEPT

    Page Should Not Contain    Testilähde

*** Keywords ***

Reset Citations Create Test Citation And Go To Home Page
    Reset Citations
    Create Test Citation
    Go To Home Page
