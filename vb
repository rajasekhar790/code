Sub DeleteRowsBasedOnList()
    Dim keySheet As Worksheet
    Dim targetSheet As Worksheet
    Dim keyRange As Range
    Dim targetRange As Range
    Dim keyCell As Range
    Dim targetCell As Range
    Dim foundCell As Range

    ' Set references to the sheets
    Set keySheet = ThisWorkbook.Sheets("Sheet1") ' The sheet with the list of keys
    Set targetSheet = ThisWorkbook.Sheets("Sheet2") ' The sheet where rows will be deleted

    ' Define the range where the key values are located
    Set keyRange = keySheet.Range("A1:A10") ' Assuming keys are in A1:A10 on Sheet1

    ' Loop through each key value
    For Each keyCell In keyRange
        If Not IsEmpty(keyCell.Value) Then
            ' Look for the key value in the target sheet
            Set foundCell = targetSheet.Columns("A:A").Find(What:=keyCell.Value, LookIn:=xlValues, LookAt:=xlWhole)

            ' If the key value is found, delete the entire row
            If Not foundCell Is Nothing Then
                Do
                    foundCell.EntireRow.Delete
                    ' Try to find next occurrence
                    Set foundCell = targetSheet.Columns("A:A").FindNext(After:=foundCell)
                Loop While Not foundCell Is Nothing And foundCell.Address <> targetSheet.Columns("A:A").Find(What:=keyCell.Value, LookIn:=xlValues, LookAt:=xlWhole).Address
            End If
        End If
    Next keyCell
End Sub