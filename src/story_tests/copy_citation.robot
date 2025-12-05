*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations And Go To Home Page

*** Test Cases ***

Copy Citations To Clipboard With One Citation Created
    Create Test Citation And Go To Home Page
    Click Button  Copy to clipboard
    Page Should Contain  Bibtex copied to clipboard

Copy Citations To Clipboard With Two Citations Created
    Create Two Test Citations And Go To Home Page
    Scroll Element Into View    id=copy_all_button
    Wait Until Element Is Visible    id=copy_all_button
    Click Button    copy_all_button
    Page Should Contain  Bibtex copied to clipboard

Copy Citations To Clipboard With No Citations Created
    Element Should Be Disabled  id=copy_all_button

Copy Single Citation To Clipboard
    Create Test Citation And Go To Home Page
    Click Link  Testilähde
    Page Should Contain    Details
    Scroll Element Into View    id=copy_bib_button
    Wait Until Element Is Visible    id=copy_bib_button
    Click Button    copy_bib_button
    Page Should Contain  Bibtex copied to clipboard

*** Keywords ***

Reset Citations And Go To Home Page
    Reset Citations
    Go To Home Page

Create Test Citation And Go To Home Page
    Create Test Citation
    Go To Home Page

Create Two Test Citations And Go To Home Page
    Create Two Test Citations
    Go To Home Page

